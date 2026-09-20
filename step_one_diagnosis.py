import pandas as pd

# Load dataset
df = pd.read_excel('Shyan_Synthetic_Travel_Cost_Data.xlsx', sheet_name='Trips')

# 1. Demand Metrics
r_dist = df['Distance_km'].corr(df['Total_Trip_Cost_GBP'])
meeting_cost = df[df['Trip_Purpose'] == 'Client meeting']['Total_Trip_Cost_GBP'].mean()
delivery_cost = df[df['Trip_Purpose'] == 'Project delivery']['Total_Trip_Cost_GBP'].mean()

# 2. Price Metrics
hotel_peak = df[df['Event_Peak_Flag'] == 'Yes']['Hotel_Rate_GBP_per_Night'].mean()
hotel_std = df[df['Event_Peak_Flag'] == 'No']['Hotel_Rate_GBP_per_Night'].mean()
biz_fare = df[df['Cabin_Class'] == 'Business']['Base_Fare_GBP'].mean()
econ_fare = df[df['Cabin_Class'] == 'Economy']['Base_Fare_GBP'].mean()
biz_count = (df['Cabin_Class'] == 'Business').sum()

# 3. Process Metrics
r_approval = df['Approval_Days'].corr(df['Booking_Lead_Days'])
fare_0_3 = df[df['Advance_Purchase_Band'] == '0-3 days']['Base_Fare_GBP'].mean()
fare_15_30 = df[df['Advance_Purchase_Band'] == '15-30 days']['Base_Fare_GBP'].mean()

# 4. Behavioural Metrics
non_comp_cost = df[df['Policy_Compliant'] == 'No']['Total_Trip_Cost_GBP'].mean()
comp_cost = df[df['Policy_Compliant'] == 'Yes']['Total_Trip_Cost_GBP'].mean()
non_comp_count = (df['Policy_Compliant'] == 'No').sum()

# Build DataFrame
drivers = pd.DataFrame([
    {
        "Category": "Demand",
        "Driver": "Route Distance",
        "Evidence (Synthetic Data)": f"r = {r_dist:.2f} correlation with total spend",
        "Operational Mechanism": "Longer flight routes require structurally higher fuel and base ticketing costs."
    },
    {
        "Category": "Demand",
        "Driver": "Trip Purpose",
        "Evidence (Synthetic Data)": f"Client meetings £{meeting_cost:,.2f} vs Delivery £{delivery_cost:,.2f}",
        "Operational Mechanism": "Commercial/revenue-generating trips involve premium hub destinations and inflexible schedules."
    },
    {
        "Category": "Price",
        "Driver": "Peak Surge Pricing",
        "Evidence (Synthetic Data)": f"£{hotel_peak:.2f}/night (peak) vs £{hotel_std:.2f} (standard)",
        "Operational Mechanism": "Dynamic supplier pricing during market event spikes imposes a 24.1% hotel rate premium."
    },
    {
        "Category": "Price",
        "Driver": "Cabin Class Mix",
        "Evidence (Synthetic Data)": f"Business £{biz_fare:,.2f} vs Economy £{econ_fare:,.2f} ({biz_count} trips)",
        "Operational Mechanism": "Premium cabin selection multiplies base airfare by 3.5x over standard economy seats."
    },
    {
        "Category": "Process",
        "Driver": "Approval Friction",
        "Evidence (Synthetic Data)": f"r = {r_approval:.2f} with booking lead time",
        "Operational Mechanism": "Internal management sign-off bottlenecks compress the available advance booking window."
    },
    {
        "Category": "Process",
        "Driver": "Late Booking Penalty",
        "Evidence (Synthetic Data)": f"0-3d: £{fare_0_3:,.2f} vs 15-30d: £{fare_15_30:,.2f}",
        "Operational Mechanism": "Purchasing within 72 hours triggers an average £433.65 yield penalty per flight."
    },
    {
        "Category": "Behavioural",
        "Driver": "Policy Non-Compliance",
        "Evidence (Synthetic Data)": f"Non-compliant £{non_comp_cost:,.2f} vs Compliant £{comp_cost:,.2f} ({non_comp_count} trips)",
        "Operational Mechanism": "Booking outside company-negotiated inventory adds £488.71 of excess cost per trip."
    }
])

markdown_table = drivers.to_markdown(index=False)

readme_content = f"""# Travel Cost & Systems Optimisation Challenge

Educational project analysing business travel spend, root-cause process delays, Causal Loop Diagrams (CLD), and monthly forecasting.

## 1. Diagnose the System: Spend Drivers

{markdown_table}
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("Step 1 complete: README.md updated successfully.")