# Travel Cost & Systems Optimisation Challenge

Educational project analysing business travel spend, root-cause process delays, Causal Loop Diagrams (CLD), and monthly forecasting.

## 1. Diagnose the System: Spend Drivers

| Category    | Driver                | Evidence (Synthetic Data)                                  | Operational Mechanism                                                                          |
|:------------|:----------------------|:-----------------------------------------------------------|:-----------------------------------------------------------------------------------------------|
| Demand      | Route Distance        | r = 0.66 correlation with total spend                      | Longer flight routes require structurally higher fuel and base ticketing costs.                |
| Demand      | Trip Purpose          | Client meetings £2,108.09 vs Delivery £1,931.15            | Commercial/revenue-generating trips involve premium hub destinations and inflexible schedules. |
| Price       | Peak Surge Pricing    | £224.10/night (peak) vs £180.60 (standard)                 | Dynamic supplier pricing during market event spikes imposes a 24.1% hotel rate premium.        |
| Price       | Cabin Class Mix       | Business £3,159.52 vs Economy £897.86 (176 trips)          | Premium cabin selection multiplies base airfare by 3.5x over standard economy seats.           |
| Process     | Approval Friction     | r = -0.10 with booking lead time                           | Internal management sign-off bottlenecks compress the available advance booking window.        |
| Process     | Late Booking Penalty  | 0-3d: £1,319.20 vs 15-30d: £885.54                         | Purchasing within 72 hours triggers an average £433.65 yield penalty per flight.               |
| Behavioural | Policy Non-Compliance | Non-compliant £2,404.26 vs Compliant £1,915.56 (460 trips) | Booking outside company-negotiated inventory adds £488.71 of excess cost per trip.             |
