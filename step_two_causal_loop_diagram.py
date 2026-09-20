import os
import re

# 1. Clean, balanced Mermaid Diagram without rigid subgraph collision
mermaid_diagram = """```mermaid
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
```"""

# 2. Documentation using clean unicode arrows (no string escape bugs)
step_2_block = f"""## 2. Systems Thinking: Causal Loop Diagram (CLD)

{mermaid_diagram}

### System Architecture: 12 Variables, Loops & Mechanisms

#### The 12 Variables
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
  * **System Insight:** Bureaucratic governance designed to restrict spending inadvertently increases ticket prices by stripping employees of advance purchase discounts.

* **$R_2$: The Volatility Trap (Reinforcing Loop — Early Booking Flexibility Penalty)**
  * **Mechanism:** Mandating advance bookings ($+$ Lead Time) → Increases exposure to client schedule changes and project date shifts ($+$ Schedule Uncertainty) → Higher rate of flight modifications and cancellations ($+$) → Change & Cancellation Fees rise ($+$) → Total Spend rises ($+$).
  * **System Insight:** Advance booking discounts carry a real operational trade-off against schedule churn; booking too far out can inflate change fees.

* **$B_1$: Virtual Substitution (Balancing Loop — Demand Dampening)**
  * **Mechanism:** Budget Pressure ($+$) → Virtual Meeting Substitution rises ($+$) → Travel Requests Initiated falls ($-$) → Total Travel Spend drops ($-$).
  * **System Insight:** Rising cost pressure naturally pushes teams toward digital alternatives for routine internal collaboration.

* **$B_2$: Discretionary Trip Pruning (Balancing Loop — Governance Intervention)**
  * **Mechanism:** Budget Pressure ($+$) → Management rejects non-essential travel ($+$) → Discretionary requests fall ($-$) → Total Travel Spend drops ($-$)."""

# 3. Update README.md strictly between Step 2 delimiters
readme_filename = "README.md"
if not os.path.exists(readme_filename):
    raise FileNotFoundError("README.md not found in the current directory.")

with open(readme_filename, "r", encoding="utf-8") as f:
    readme_content = f.read()

pattern = r"<!-- STEP_2_START -->.*?<!-- STEP_2_END -->"
replacement = f"<!-- STEP_2_START -->\n{step_2_block}\n<!-- STEP_2_END -->"

if "<!-- STEP_2_START -->" in readme_content:
    updated_readme = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)
else:
    updated_readme = readme_content + f"\n\n<!-- STEP_2_START -->\n{step_2_block}\n<!-- STEP_2_END -->\n"

with open(readme_filename, "w", encoding="utf-8") as f:
    f.write(updated_readme)

print("Step 2 refreshed: diagram layout corrected and arrows rendered cleanly.")