# Travel Cost & Systems Optimisation Challenge

An educational analytics project connecting business operations, systems thinking, dynamic cost-driver analysis, and spend forecasting.

---

<!-- STEP_1_START -->
## 1. Diagnose the System: Spend Drivers

| Category    | Driver                | Evidence (Synthetic Data)                                  | Operational Mechanism                                                                                 |
|:------------|:----------------------|:-----------------------------------------------------------|:------------------------------------------------------------------------------------------------------|
| Demand      | Route Distance        | r = 0.66 correlation with total spend                      | Longer flight routes require structurally higher fuel and base ticketing costs.                       |
| Demand      | Trip Purpose          | Client meetings £2,108.09 vs Delivery £1,931.15            | Commercial and client-facing trips involve premium hub destinations and inflexible arrival schedules. |
| Price       | Peak Surge Pricing    | £224.10/night (peak) vs £180.60 (standard)                 | Dynamic hotel inventory algorithms during city-wide event windows impose a 24.1% rate premium.        |
| Price       | Cabin Class Mix       | Business £3,159.52 vs Economy £897.86 (176 trips)          | Premium cabin selection multiplies baseline airfare by 3.5x across commercial travel.                 |
| Process     | Approval Friction     | r = -0.10 with booking lead time                           | Multi-day management approval bottlenecks compress the available advance booking window.              |
| Process     | Late Booking Penalty  | 0-3d: £1,319.20 vs 15-30d: £885.54                         | Booking within 72 hours triggers an average £433.65 yield penalty per flight.                         |
| Behavioural | Policy Non-Compliance | Non-compliant £2,404.26 vs Compliant £1,915.56 (460 trips) | Booking outside negotiated channels or policy caps adds £488.71 of excess cost per trip.              |

### Key Diagnostic Takeaways
* **Structural Baseline:** Route distance ($r = 0.66$) and duration ($r = 0.42$) dictate the baseline demand, which are unavoidable unless you are willing to directly affect the business.
* **Compounding Process Bottlenecks:** Management approval delays compress booking lead windows, forcing travellers into high-cost, short-notice tiers that add an average £433.65 surcharge per ticket.
* **Controllable Price & Behavioural Leakage:** Premium cabin selections, peak event hotel surges, and policy non-compliance (£488.71 excess cost per non-compliant trip) drive avoidable financial leakage that targeted interventions can capture without a blanket travel freeze.
<!-- STEP_1_END -->

---

