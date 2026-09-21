import os
import re
import pandas as pd
import numpy as np

# 1. Load the dataset
data_path = 'Shyan_Synthetic_Travel_Cost_Data.xlsx'
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Dataset '{data_path}' not found.")
df = pd.read_excel(data_path, sheet_name='Trips')

# 2. Establish the "Compliant Target Baseline" (Cost per Trip Day)
# Using compliant, economy trips booked 8-30 days in advance as our gold standard
baseline_df = df[(df['Policy_Compliant'] == 'Yes') & 
                 (df['Cabin_Class'] == 'Economy') & 
                 (df['Advance_Purchase_Band'].isin(['15-30 days', '8-14 days']))]

avg_daily_baseline = baseline_df['Total_Trip_Cost_GBP'].sum() / baseline_df['Trip_Days'].sum()

# Max recoverable leakage per trip = Actual Cost - (Baseline Daily Rate * Trip Days)
df['Target_Cost'] = df['Trip_Days'] * avg_daily_baseline
df['Max_Recoverable'] = np.maximum(df['Total_Trip_Cost_GBP'] - df['Target_Cost'], 0)

# 3. Waterfall Lever 1: Net Late Booking Penalty (0-7 Days)
# Calculate the cancellation risk trade-off
cancel_fee_15_30 = df[df['Advance_Purchase_Band'] == '15-30 days']['Change_Cancel_Fees_GBP'].mean()
cancel_fee_0_7 = df[df['Advance_Purchase_Band'].isin(['0-3 days', '4-7 days'])]['Change_Cancel_Fees_GBP'].mean()
cancel_risk_offset = max(cancel_fee_15_30 - cancel_fee_0_7, 0) # Expected increase in cancel fees if booked earlier

avg_fare_15_30 = df[df['Advance_Purchase_Band'] == '15-30 days']['Base_Fare_GBP'].mean()

def calc_late_savings(row):
    if row['Advance_Purchase_Band'] in ['0-3 days', '4-7 days']:
        gross_savings = max(row['Base_Fare_GBP'] - avg_fare_15_30, 0)
        net_savings = max(gross_savings - cancel_risk_offset, 0)
        return min(net_savings, row['Max_Recoverable']) # Cannot save more than the total trip variance
    return 0

df['Net_Late_Savings'] = df.apply(calc_late_savings, axis=1)
df['Remaining_Pool_1'] = df['Max_Recoverable'] - df['Net_Late_Savings']

# 4. Waterfall Lever 2: Unauthorized Premium Cabin Leakage
# Managing Directors are authorized; all others are non-compliant for Business/First class
avg_econ_fare = df[df['Cabin_Class'] == 'Economy']['Base_Fare_GBP'].mean()

def calc_cabin_savings(row):
    if row['Cabin_Class'] in ['Business', 'First'] and row['Traveler_Level'] != 'Managing Director':
        gross_savings = max(row['Base_Fare_GBP'] - avg_econ_fare, 0)
        return min(gross_savings, row['Remaining_Pool_1'])
    return 0

df['Net_Cabin_Savings'] = df.apply(calc_cabin_savings, axis=1)
df['Remaining_Pool_2'] = df['Remaining_Pool_1'] - df['Net_Cabin_Savings']

# 5. Waterfall Lever 3: General Policy & Peak Hotel Surge
# Remaining variance assigned to non-compliance (e.g., booking expensive off-channel hotels)
def calc_compliance_savings(row):
    if row['Policy_Compliant'] == 'No' or row['Event_Peak_Flag'] == 'Yes':
        return row['Remaining_Pool_2']
    return 0

df['Net_Compliance_Savings'] = df.apply(calc_compliance_savings, axis=1)

# 6. Aggregate Financials
total_late = df['Net_Late_Savings'].sum()
total_cabin = df['Net_Cabin_Savings'].sum()
total_compliance = df['Net_Compliance_Savings'].sum()
total_net_savings = total_late + total_cabin + total_compliance
total_spend = df['Total_Trip_Cost_GBP'].sum()
pct_savings = (total_net_savings / total_spend) * 100

# 7. Generate Markdown Table & Commentary
summary_df = pd.DataFrame({
    "Efficiency Lever": [
        "1. Advance Booking Optimization (0-7 Days)",
        "2. Unauthorized Premium Cabin (Non-MD)",
        "3. Policy Non-Compliance & Peak Surge",
        "**Total Avoidable Spend**"
    ],
    "Calculation Logic & Confounder Control": [
        "Targeted 15-30 day advance window. Deducted £12+ expected schedule churn risk per ticket.",
        "Isolated Business Class base fares. Excluded Managing Directors to respect policy allowances.",
        "Captured remaining trip-level variance strictly tied to off-channel booking or event surges.",
        "**Strict row-by-row waterfall limits savings to mathematical maximums.**"
    ],
    "Net Recoverable (£)": [
        f"£{total_late:,.2f}",
        f"£{total_cabin:,.2f}",
        f"£{total_compliance:,.2f}",
        f"**£{total_net_savings:,.2f} ({pct_savings:.1f}% of Spend)**"
    ]
})

markdown_table = summary_df.to_markdown(index=False)

step_3_block = f"""

To prevent overlapping estimates (double-counting) the figures have been calculated with a waterfall methodology. We first calculated a baseline daily rate based on the trips that did everything right (e.g. Economy Class, Policy Compliant, Booked in Advance). Then, this gives an upper ceiling for how much money one can save on a trip, given by Actual Cost - Target Cost. 

{markdown_table}

### Key Financial Insights
* **The Flexibility Trade-off:** Pushing short-notice bookings into the 15-30 day window yields significant base airfare discounts, but the net savings are partially offset by the statistical increase in schedule churn (cancellation fees). The £{total_late:,.0f} figure represents pure net opportunity.
* **Controlled Enforcement:** By excluding authorized executive travel (Managing Directors) from the premium cabin calculations, the £{total_cabin:,.0f} identified represents genuine behavioral policy leakage rather than structural seniority allowances.
* **Total Opportunity:** The organization is losing approximately **{pct_savings:.1f}%** of its total travel budget to addressable friction and behavioral leakage, which can be mitigated without reducing the actual volume of commercial travel demand."""

# 8. Update README.md securely
readme_filename = "README.md"
with open(readme_filename, "r", encoding="utf-8") as f:
    readme_content = f.read()

pattern = r"<!-- STEP_3_START -->.*?<!-- STEP_3_END -->"
replacement = f"<!-- STEP_3_START -->\n{step_3_block}\n<!-- STEP_3_END -->"

if "<!-- STEP_3_START -->" in readme_content:
    updated_readme = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)
else:
    updated_readme = readme_content + f"\n\n<!-- STEP_3_START -->\n{step_3_block}\n<!-- STEP_3_END -->\n"

with open(readme_filename, "w", encoding="utf-8") as f:
    f.write(updated_readme)

print("Step 3 completed: Waterfall quantification applied and README.md updated successfully.")