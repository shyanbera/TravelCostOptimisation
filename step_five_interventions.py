import os
import re
import pandas as pd

# 1. Define the Interventions Data
interventions_data = {
    "Intervention": [
        "1. The Advance Booking Lock",
        "2. Premium Cabin Hard-Cap",
        "3. Volatility Flex-Fare Mandate"
    ],
    "Mechanism (The Fix)": [
        "Reconfigure booking software to require VP-level approval for any flight booked <7 days before departure.",
        "Systemic rejection of Business/First Class fares at the software level for any profile not flagged as 'Managing Director'.",
        "Mandate the purchase of fully refundable (flex) fares strictly for client-facing teams with historical cancellation rates >20%."
    ],
    "Expected Impact": [
        "Shifts 40% of short-notice bookings into the 8-14 day window, capturing a portion of the avoidable late-booking spend.",
        "Recovers 100% of the unauthorized premium cabin leakage identified in Step 3.",
        "Neutralizes the financial damage of the $R_2$ Volatility Loop by eliminating £150+ change fees for high-risk trips."
    ],
    "Downside Risk": [
        "Approval delays (the $R_1$ loop) could cause employees to miss urgent, high-value client deals.",
        "Employee dissatisfaction and potential churn among high-frequency, non-MD traveling staff.",
        "If cancellation rates unexpectedly drop, the company loses money paying for flex-fare premiums they didn't use."
    ],
    "Leading Indicator (Input)": [
        "% of total flights booked >14 days in advance (tracked weekly).",
        "Number of rejected premium cabin booking attempts in the system.",
        "Ratio of flex vs. non-flex tickets booked by target teams."
    ],
    "Lagging KPI (Output)": [
        "Average Base Fare Cost per trip.",
        "Average Ticket Price (ATP) segmented by non-MD traveler levels.",
        "Total Net Cost per Trip (Base Fare + Penalty Fees)."
    ],
    "Causality Test": [
        "**Difference-in-Differences:** Staggered rollout. Pilot in Marketing; use Sales as the control group to isolate the policy's effect from market trends.",
        "**Interrupted Time Series:** Track daily ATP for non-MDs. Look for an immediate, structural break in the trendline on the exact go-live date.",
        "**A/B Test:** Apply mandate to Consulting Team A, keep Consulting Team B on standard rules. Compare net trip costs after 3 months."
    ]
}

df_interventions = pd.DataFrame(interventions_data)
markdown_table = df_interventions.to_markdown(index=False)

# 2. Construct the Markdown Block
step_5_block = f"""

Based on the leakage quantified in Step 3 and the system dynamics mapped in Step 2, the following three interventions are designed to structurally reduce avoidable spend. To ensure data science rigor, each intervention includes a specific statistical method to test causality, separating the true impact of the policy from background market noise.

{markdown_table}"""

# 3. Update README.md securely
readme_filename = "README.md"
if not os.path.exists(readme_filename):
    with open(readme_filename, "w", encoding="utf-8") as f:
        f.write("")

with open(readme_filename, "r", encoding="utf-8") as f:
    readme_content = f.read()

pattern = r"<!-- STEP_5_START -->.*?<!-- STEP_5_END -->"
replacement = f"<!-- STEP_5_START -->\n{step_5_block}\n<!-- STEP_5_END -->"

if "<!-- STEP_5_START -->" in readme_content:
    updated_readme = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)
else:
    updated_readme = readme_content + f"\n\n<!-- STEP_5_START -->\n{step_5_block}\n<!-- STEP_5_END -->\n"

with open(readme_filename, "w", encoding="utf-8") as f:
    f.write(updated_readme)

print("Step 5 complete: Interventions table generated and written to README.md.")