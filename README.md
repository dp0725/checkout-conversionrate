# Diagnosing a Drop in Checkout Conversion (Product Analytics Case Study)

## Problem
Over the last 14 days, the product team observed a **~15% drop in checkout conversion**.  
As the Product Data Scientist, I will diagnose where the drop occurs in the funnel, identify the most likely drivers, and recommend actions with clear monitoring metrics.

## Why It Matters
Checkout conversion is a direct driver of revenue and customer trust. A sustained decline can indicate:
- funnel friction (UX regression)
- technical issues (latency, errors, payment failures)
- traffic mix shifts (lower-intent acquisition)
- instrumentation / tracking issues (data quality)

The goal is to isolate the **root cause** quickly and provide **decision-ready recommendations**.

## Data
This project uses **synthetic event-level data** that mimics a typical e-commerce funnel:
`visit → product_view → add_to_cart → checkout → purchase`

The dataset includes common explanatory dimensions:
- device (mobile/desktop)
- geo
- traffic_source
- new vs returning users
- app_version (release-driven effects)
- page_load_ms
- payment_method
- event timestamps

## Approach
1. **Define funnel & success metrics**
   - step conversion rates
   - overall checkout conversion
   - guardrails (e.g., latency, payment failures)

2. **Localize the drop**
   - compare “baseline” vs “recent” windows
   - identify the funnel step(s) with the largest relative degradation

3. **Segment & diagnose**
   - cut by device / geo / source / user type / app_version
   - isolate concentrated impact (where + when)

4. **Hypothesis testing (decision-oriented)**
   - evaluate candidate causes (release, latency, payment failures, traffic mix)
   - quantify contribution where possible (decomposition by segment)

5. **Recommendations & monitoring**
   - actions prioritized by expected impact and confidence
   - define dashboards / alerts to prevent recurrence

## Key Findings (to be filled)
- Where in the funnel the drop is concentrated:
- Segments most impacted:
- Primary driver(s):
- Evidence supporting root cause:

## Recommendations (to be filled)
- Immediate mitigation:
- Short-term fixes:
- Longer-term prevention:

## Monitoring Plan
- North star: checkout conversion (purchase / visit)
- Step conversions: view→cart, cart→checkout, checkout→purchase
- Guardrails: page load latency, payment failure rate, error rate
- Diagnostics cuts: device, app_version, traffic_source, geo, new/returning

## Repo Structure
- `data/` synthetic datasets
- `sql/` funnel & segment queries (authoritative metrics)
- `notebooks/` analysis & visualization
- `analysis/` writeups, methodology, decisions
- `charts/` exported visuals
- `insights.md` executive summary (1-page)

## Executive Summary
See `insights.md` for the final decision-ready summary.
