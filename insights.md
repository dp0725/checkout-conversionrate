# Executive Summary — Checkout Conversion Drop

## What happened
- Checkout conversion decreased by ~X% starting around YYYY-MM-DD.

## Where it happened (funnel localization)
- The largest relative decline occurred at: **checkout → purchase**
- Other steps were stable / minor changes.

## Who it impacted (segments)
Top impacted segments:
1. Mobile + app_version 2.0.x
2. New users
3. [Geo/Source if applicable]

## Why it happened (root cause)
Most likely driver(s):
- Increased page load latency on mobile coinciding with release 2.0.x
- Resulting in lower completion in checkout → purchase

## Recommended actions
1. Roll back / patch checkout flow for mobile 2.0.x
2. Add performance budget & monitoring for checkout latency
3. Add guardrail alerts: payment failures, error rate, latency p95

## Confidence & risks
- Confidence: High/Medium/Low
- Risks / alternative explanations:
- Data quality checks performed:
