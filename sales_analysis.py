"""
Week 3: Sales Data Analysis
Files required: sales_analysis.py, sales_data.csv, analysis_report.md, requirements.txt
Run: python sales_analysis.py
"""

import pandas as pd

# Sample code from the project instructions
df = pd.read_csv("sales_data.csv")
total_revenue = df["Total_Sales"].sum()
print(f"Total Revenue: ${total_revenue:,.2f}")

# Explore the dataset
print("\nDataset Preview:")
print(df.head())
print(f"\nRows: {df.shape[0]} | Columns: {df.shape[1]}")
print("\nMissing Values:")
print(df.isnull().sum())

# Clean the data
df = df.drop_duplicates().copy()

for column in ["Quantity", "Unit_Price", "Total_Sales"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df["Product"] = df["Product"].fillna("Unknown").astype(str).str.strip()
df.loc[df["Product"] == "", "Product"] = "Unknown"
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Fill missing sales totals when quantity and unit price are available
missing_total = df["Total_Sales"].isna()
can_calculate = df["Quantity"].notna() & df["Unit_Price"].notna()
df.loc[missing_total & can_calculate, "Total_Sales"] = (
    df.loc[missing_total & can_calculate, "Quantity"]
    * df.loc[missing_total & can_calculate, "Unit_Price"]
)

df = df.dropna(subset=["Date", "Quantity", "Unit_Price", "Total_Sales"])
df = df[
    (df["Quantity"] > 0)
    & (df["Unit_Price"] >= 0)
    & (df["Total_Sales"] >= 0)
].copy()

# Recalculate totals to keep the data consistent
df["Total_Sales"] = (df["Quantity"] * df["Unit_Price"]).round(2)

# Calculate key metrics
total_revenue = df["Total_Sales"].sum()
total_units = int(df["Quantity"].sum())
average_sale = df["Total_Sales"].mean()
highest_sale = df["Total_Sales"].max()
lowest_sale = df["Total_Sales"].min()

# Summarize performance by product
product_sales = (
    df.groupby("Product")
    .agg(
        Units_Sold=("Quantity", "sum"),
        Transactions=("Product", "count"),
        Revenue=("Total_Sales", "sum"),
    )
    .sort_values("Revenue", ascending=False)
)

best_product = product_sales["Revenue"].idxmax()
best_revenue = product_sales["Revenue"].max()
top_units_product = product_sales["Units_Sold"].idxmax()

print("\nKEY SALES METRICS")
print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Total Units Sold: {total_units:,}")
print(f"Average Sale: ${average_sale:,.2f}")
print(f"Highest Sale: ${highest_sale:,.2f}")
print(f"Lowest Sale: ${lowest_sale:,.2f}")

print("\nPRODUCT PERFORMANCE")
print(product_sales.to_string(float_format=lambda value: f"{value:,.2f}"))

# Save the cleaned dataset and product summary
df.to_csv("cleaned_sales_data.csv", index=False)
product_sales.to_csv("product_sales_summary.csv")

# Create a professional Markdown report
report = f"""# Sales Data Analysis Report

## Project Overview
This project uses Python and pandas to explore, clean, and analyze a sample sales dataset.

## Dataset Summary
- Valid transactions analyzed: {len(df)}
- Number of products: {df["Product"].nunique()}
- Date range: {df["Date"].min().date()} to {df["Date"].max().date()}

## Key Metrics
- **Total revenue:** ${total_revenue:,.2f}
- **Total units sold:** {total_units:,}
- **Average transaction value:** ${average_sale:,.2f}
- **Highest transaction:** ${highest_sale:,.2f}
- **Lowest transaction:** ${lowest_sale:,.2f}

## Product Performance

{product_sales.to_string()}

## Key Findings
- **Top product by revenue:** {best_product} (${best_revenue:,.2f}).
- **Top product by units sold:** {top_units_product}.
- The average transaction value was ${average_sale:,.2f}.

## Recommendations
1. Monitor stock levels for products generating the most revenue.
2. Review lower-revenue products before making pricing or promotion decisions.
3. Track revenue and units sold regularly to compare performance over time.

## Limitations
This is a practice dataset. The results describe the supplied records and do not prove why customers purchased a product.
"""

with open("analysis_report.md", "w", encoding="utf-8") as file:
    file.write(report)

print("\nProject completed successfully.")
print("Generated files: analysis_report.md, cleaned_sales_data.csv, product_sales_summary.csv")
