import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def generate_synthetic_funnel(n_users=30000, days=60):
    end = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start = end - timedelta(days=days)

    # user table
    user_id = np.arange(1, n_users + 1)
    is_new = np.random.binomial(1, 0.55, n_users)
    device = np.random.choice(["mobile", "desktop"], size=n_users, p=[0.7, 0.3])
    geo = np.random.choice(["US", "IN", "EU", "BR", "OTHER"], size=n_users, p=[0.35, 0.25, 0.2, 0.1, 0.1])
    traffic_source = np.random.choice(["organic", "paid_search", "paid_social", "referral", "email"], size=n_users,
                                      p=[0.35, 0.25, 0.2, 0.1, 0.1])
    payment_method = np.random.choice(["card", "upi", "paypal", "cod"], size=n_users, p=[0.55, 0.2, 0.15, 0.1])

    users = pd.DataFrame({
        "user_id": user_id,
        "is_new": is_new,
        "device": device,
        "geo": geo,
        "traffic_source": traffic_source,
        "payment_method": payment_method,
    })

    # assign each user a "session day"
    day_offsets = np.random.randint(0, days, n_users)
    session_date = start + pd.to_timedelta(day_offsets, unit="D")
    users["session_date"] = session_date

    # app_version: newer version rolled out recently (last 14 days)
    users["is_recent_window"] = (users["session_date"] >= (end - timedelta(days=14))).astype(int)
    users["app_version"] = np.where(users["is_recent_window"].eq(1) & (users["device"].eq("mobile")),
                                    np.random.choice(["2.0.0", "2.0.1"], size=n_users, p=[0.7, 0.3]),
                                    np.random.choice(["1.9.0", "1.9.1"], size=n_users, p=[0.6, 0.4]))

    # latency: higher on mobile in recent window (simulates performance regression)
    base_load = np.where(users["device"].eq("mobile"), 1600, 900)
    recent_penalty = np.where((users["device"].eq("mobile")) & (users["is_recent_window"].eq(1)), 500, 0)
    noise = np.random.normal(0, 220, n_users)
    users["page_load_ms"] = np.clip(base_load + recent_penalty + noise, 200, 6000).astype(int)

    # Funnel probabilities with interpretable drivers
    # visit -> product_view
    p_view = sigmoid(2.2
                     - 0.00035 * (users["page_load_ms"] - 1000)
                     + 0.15 * (users["traffic_source"].eq("organic").astype(int))
                     - 0.10 * (users["traffic_source"].eq("paid_social").astype(int)))

    # product_view -> add_to_cart
    p_cart = sigmoid(1.1
                     - 0.00045 * (users["page_load_ms"] - 1000)
                     + 0.18 * (1 - users["is_new"])
                     - 0.12 * (users["device"].eq("mobile").astype(int)))

    # add_to_cart -> checkout
    p_checkout = sigmoid(1.0
                         - 0.00040 * (users["page_load_ms"] - 1000)
                         + 0.12 * (users["traffic_source"].eq("email").astype(int)))

    # checkout -> purchase (inject the “drop” here)
    # recent window + mobile + new version increases friction
    version_penalty = np.where((users["device"].eq("mobile")) & (users["is_recent_window"].eq(1)), 0.55, 0.0)
    p_purchase = sigmoid(1.0
                         - 0.00055 * (users["page_load_ms"] - 1000)
                         - version_penalty
                         - 0.10 * (users["payment_method"].eq("cod").astype(int)))

    # simulate funnel
    users["did_view"] = np.random.binomial(1, p_view)
    users["did_cart"] = np.random.binomial(1, p_cart) * users["did_view"]
    users["did_checkout"] = np.random.binomial(1, p_checkout) * users["did_cart"]
    users["did_purchase"] = np.random.binomial(1, p_purchase) * users["did_checkout"]

    # build event table
    events = []
    for _, r in users.iterrows():
        # one session, ordered events
        t0 = r["session_date"] + timedelta(minutes=int(np.random.randint(0, 1440)))
        def add_event(name, t):
            events.append({
                "user_id": int(r["user_id"]),
                "event_time": t,
                "event_name": name,
                "device": r["device"],
                "geo": r["geo"],
                "traffic_source": r["traffic_source"],
                "is_new": int(r["is_new"]),
                "app_version": r["app_version"],
                "page_load_ms": int(r["page_load_ms"]),
                "payment_method": r["payment_method"],
            })

        add_event("visit", t0)
        if r["did_view"]:
            add_event("product_view", t0 + timedelta(minutes=2))
        if r["did_cart"]:
            add_event("add_to_cart", t0 + timedelta(minutes=6))
        if r["did_checkout"]:
            add_event("checkout", t0 + timedelta(minutes=10))
        if r["did_purchase"]:
            add_event("purchase", t0 + timedelta(minutes=14))

    events_df = pd.DataFrame(events).sort_values(["user_id", "event_time"]).reset_index(drop=True)
    return users, events_df

if __name__ == "__main__":
    users_df, events_df = generate_synthetic_funnel(n_users=30000, days=60)
    users_df.to_csv("data/users.csv", index=False)
    events_df.to_csv("data/events.csv", index=False)
    print("Wrote data/users.csv and data/events.csv")
    print("Events:", len(events_df), "Users:", len(users_df))
