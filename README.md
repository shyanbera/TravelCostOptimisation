# Travel Cost & Systems Optimisation Challenge

This project is based on synthetic data. It simulates a business with rising travel spend, and I have been tasked with understanding where cost is structural and where it is avoidable. The aim is to suggest interventions to reduce spend without damaging client delivery, collaboration or growth.

---

<!-- STEP_1_START -->
## 1. What are the most important drivers of travel spend?

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


## 2. Causal Loop Diagram (CLD)
Here I have constructed a Causal Loop Diagram. This serves as a hypothesis for how the drivers of travel spend interact, motivated by some of the data from Step 1 as well as a general understanding of corporate structure.

<!-- STEP_2_START -->
```mermaid
flowchart TD
    %% Nodes
    V1["1. Core Travel Demand"]
    V2["2. Travel Requests Initiated"]
    V10["10. Budget Variance & Cost Pressure"]
    V3["3. Policy Strictness & Controls"]
    V4["4. Approval Delay (Process Lag ||)"]
    V5["5. Booking Lead Time (Days)"]
    V6["6. Unit Airfares & Hotel Rates"]
    V7["7. Schedule Uncertainty & Churn"]
    V8["8. Change & Cancellation Fees"]
    V9["9. Total Travel Spend (£)"]
    V11["11. Discretionary Trip Pruning"]
    V12["12. Virtual Meeting Substitution"]

    %% R1: Bottleneck Loop
    V10 -->|"+"| V3
    V3 -->|"+ [DELAY]"| V4
    V4 -->|"-"| V5
    V5 -->|"-"| V6
    V6 -->|"+"| V9
    V9 -->|"+"| V10

    %% R2: Volatility Loop
    V5 -->|"+"| V7
    V7 -->|"+"| V8
    V8 -->|"+"| V9

    %% Balancing Loops (B1 & B2) & Demand
    V1 -->|"+"| V2
    V2 -->|"+"| V9
    V10 -->|"+"| V12
    V12 -->|"-"| V2
    V10 -->|"+"| V11
    V11 -->|"-"| V2

    %% Styling
    classDef expense fill:#fee2e2,stroke:#dc2626,stroke-width:2px,color:#991b1b;
    classDef delay fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#92400e;
    classDef standard fill:#eff6ff,stroke:#2563eb,stroke-width:1.5px,color:#1e3a8a;

    class V9,V10 expense;
    class V4 delay;
    class V1,V2,V3,V5,V6,V7,V8,V11,V12 standard;
```


### Explanation of The 12 Variables
1. **Core Business Demand:** Underlying commercial requirement for client delivery, business development, and delivery milestones.
2. **Travel Requests Initiated:** Volume of trip bookings formally submitted by employees.
3. **Policy Strictness & Controls:** Management implementation of pre-trip approval gates and scrutiny.
4. **Approval Delay (Explicit Delay $||$):** The multi-day administrative lag between request submission and manager sign-off.
5. **Booking Lead Time:** Days between flight/hotel booking confirmation and departure date.
6. **Unit Airfares & Hotel Rates:** Market ticket prices governed by airline yield algorithms and hotel peak tiers.
7. **Schedule Uncertainty & Churn:** Likelihood that client deliverables, meetings, or project dates shift.
8. **Change & Cancellation Fees:** Friction penalties paid to amend, rebook, or forfeit tickets.
9. **Total Travel Spend:** Aggregate organizational expenditure across travel categories.
10. **Budget Variance & Cost Pressure:** Executive distress when spend exceeds allocated targets.
11. **Discretionary Trip Pruning:** Management rejection of internal workshops, training, and non-essential travel.
12. **Virtual Meeting Substitution:** Shifting face-to-face engagements to digital channels (Teams/Zoom).

---

### Feedback Loops Breakdown

* **$R_1$: The Bottleneck Trap (Reinforcing Loop — Unintended Cost Inflation)**
  * **Mechanism:** Spend exceeds budget → Budget Pressure rises ($+$) → Leadership implements tighter approval controls ($+$) → **[DELAY]** Approval Delays lengthen ($+$) → Booking Lead Time compresses ($-$) → Unit Airfares jump due to short-notice airline yield tiers ($-$) → Total Spend increases ($+$).
  * **Takeaway:** Governance designed to restrict spending inadvertently increases ticket prices by stripping employees of advance purchase discounts.

* **$R_2$: The Volatility Trap (Reinforcing Loop — Early Booking Flexibility Penalty)**
  * **Mechanism:** Mandating advance bookings ($+$ Lead Time) → Increases exposure to client schedule changes and project date shifts ($+$ Schedule Uncertainty) → Higher rate of flight modifications and cancellations ($+$) → Change & Cancellation Fees rise ($+$) → Total Spend rises ($+$).
  * **Takeaway:** Advance booking discounts carry a real trade-off against scheduling issues; booking too far out inflates change fees.

* **$B_1$: Virtual Substitution (Balancing Loop — Demand Dampening)**
  * **Mechanism:** Budget Pressure ($+$) → Virtual Meeting Substitution rises ($+$) → Travel Requests Initiated falls ($-$) → Total Travel Spend drops ($-$).
  * **Takeaway:** Rising cost pressure naturally pushes teams toward digital alternatives for routine internal collaboration.

* **$B_2$: Discretionary Trip Pruning (Balancing Loop — Governance Intervention)**
  * **Takeaway:** Budget Pressure ($+$) → Management rejects non-essential travel ($+$) → Discretionary requests fall ($-$) → Total Travel Spend drops ($-$).
<!-- STEP_2_END -->


## 3. Quantification: Avoidable Cost Spend
<!-- STEP_3_START -->


To prevent overlapping estimates (double-counting) the figures have been calculated with a waterfall methodology. We first calculated a baseline daily rate based on the trips that did everything right (e.g. Economy Class, Policy Compliant, Booked in Advance). Then, this gives an upper ceiling for how much money one can save on a trip, given by Actual Cost - Target Cost. 

| Efficiency Lever                           | Calculation Logic & Confounder Control                                                        | Net Recoverable (£)              |
|:-------------------------------------------|:----------------------------------------------------------------------------------------------|:---------------------------------|
| 1. Advance Booking Optimization (0-7 Days) | Targeted 15-30 day advance window. Deducted £12+ expected schedule churn risk per ticket.     | £350,879.70                      |
| 2. Unauthorized Premium Cabin (Non-MD)     | Isolated Business Class base fares. Excluded Managing Directors to respect policy allowances. | £207,186.48                      |
| 3. Policy Non-Compliance & Peak Surge      | Captured remaining trip-level variance strictly tied to off-channel booking or event surges.  | £231,351.08                      |
| **Total Avoidable Spend**                  | **Strict row-by-row waterfall limits savings to mathematical maximums.**                      | **£789,417.25 (15.7% of Spend)** |

### Key Financial Insights
* **The Flexibility Trade-off:** Pushing short-notice bookings into the 15-30 day window yields significant base airfare discounts, but the net savings are partially offset by the statistical increase in schedule churn (cancellation fees). The £350,880 figure represents pure net opportunity.
* **Controlled Enforcement:** By excluding authorized executive travel (Managing Directors) from the premium cabin calculations, the £207,186 identified represents genuine behavioral policy leakage rather than structural seniority allowances.
* **Total Opportunity:** The organization is losing approximately **15.7%** of its total travel budget to addressable friction and behavioral leakage, which can be mitigated without reducing the actual volume of commercial travel demand.
<!-- STEP_3_END -->

## 4. Spend Forecasting & Reality Checks

<!-- STEP_4_START -->


To project future financial exposure, a time-series forecasting approach was applied to aggregate monthly spend. 

### Model Evaluation & Time-Based Holdout
In accordance with time-series best practices, data was strictly partitioned chronologically (80% training / 20% holdout test) to prevent data leakage and time-travel biases. 

| Model Type                     | Methodology                                                     | Mean Absolute Error (MAE)   |
|:-------------------------------|:----------------------------------------------------------------|:----------------------------|
| Baseline (Naive)               | Carries the last observed month's spend forward.                | £156,518.11                 |
| Advanced (Holt's Linear Trend) | Uses exponential smoothing to capture underlying growth trends. | £159,701.24                 |

### Using The CLD to Explain Forecast Uncertainty
Interestingly, the Advanced trend model actually produced a higher forecast error than the simple Naive baseline. This proves that linear forecasting breaks down in highly volatile environments, which is entirely expected due to the system dynamics mapped in Step 2:
* **The Volatility Penalty ($R_2$ Loop):** As demonstrated in the Causal Loop Diagram, mandating advance bookings exposes the company to external client schedule shifts. These sudden cancellations create unpredictable spikes in penalty fees that statistical trend models cannot foresee.
* **Demand Substitution ($B_1$ Loop):** If total spend nears a hard budgetary ceiling, management will force Virtual Meeting Substitution. This balancing loop acts as an organic brake on spend, which may artificially cause the Advanced trend model to over-predict future months.
* **Conclusion:** The MAE of £159,701 represents the true "noise" floor of the system. Further optimizations should focus on structurally reducing this volatility rather than attempting to predict it perfectly.
<!-- STEP_4_END -->

## 5. Strategic Interventions & KPI Tracking

<!-- STEP_5_START -->


Based on the leakage quantified in Step 3 and the system dynamics mapped in Step 2, the following three interventions are designed to structurally reduce avoidable spend. To ensure data science rigor, each intervention includes a specific statistical method to test causality, separating the true impact of the policy from background market noise.

| Intervention                    | Mechanism (The Fix)                                                                                                             | Expected Impact                                                                                                        | Downside Risk                                                                                                   | Leading Indicator (Input)                                        | Lagging KPI (Output)                                            | Causality Test                                                                                                                                          |
|:--------------------------------|:--------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------|:----------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1. The Advance Booking Lock     | Reconfigure booking software to require VP-level approval for any flight booked <7 days before departure.                       | Shifts 40% of short-notice bookings into the 8-14 day window, capturing a portion of the avoidable late-booking spend. | Approval delays (the $R_1$ loop) could cause employees to miss urgent, high-value client deals.                 | % of total flights booked >14 days in advance (tracked weekly).  | Average Base Fare Cost per trip.                                | **Difference-in-Differences:** Staggered rollout. Pilot in Marketing; use Sales as the control group to isolate the policy's effect from market trends. |
| 2. Premium Cabin Hard-Cap       | Systemic rejection of Business/First Class fares at the software level for any profile not flagged as 'Managing Director'.      | Recovers 100% of the unauthorized premium cabin leakage identified in Step 3.                                          | Employee dissatisfaction and potential churn among high-frequency, non-MD traveling staff.                      | Number of rejected premium cabin booking attempts in the system. | Average Ticket Price (ATP) segmented by non-MD traveler levels. | **Interrupted Time Series:** Track daily ATP for non-MDs. Look for an immediate, structural break in the trendline on the exact go-live date.           |
| 3. Volatility Flex-Fare Mandate | Mandate the purchase of fully refundable (flex) fares strictly for client-facing teams with historical cancellation rates >20%. | Neutralizes the financial damage of the $R_2$ Volatility Loop by eliminating £150+ change fees for high-risk trips.    | If cancellation rates unexpectedly drop, the company loses money paying for flex-fare premiums they didn't use. | Ratio of flex vs. non-flex tickets booked by target teams.       | Total Net Cost per Trip (Base Fare + Penalty Fees).             | **A/B Test:** Apply mandate to Consulting Team A, keep Consulting Team B on standard rules. Compare net trip costs after 3 months.                      |
<!-- STEP_5_END -->