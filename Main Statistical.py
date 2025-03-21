import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

# Set style for better visualizations
plt.style.use('ggplot')

# Read the CSV file (note: it uses semicolon as delimiter)
df = pd.read_csv('SuperstoreData1.csv', sep=';')

# Convert date columns to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%A, %d %B %Y', errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%A, %d %B %Y', errors='coerce')

# Fix numeric columns (replace comma with dot for decimal separator)
df['Sales'] = df['Sales'].str.replace(',', '.').astype(float)
df['Profit'] = df['Profit'].str.replace(',', '.').astype(float)
df['Discount'] = df['Discount'].astype(str).str.replace(',', '.').astype(float)

# Print basic info
print("Dataset Overview:")
print(f"Number of records: {len(df)}")
print(f"Date range: {df['Order Date'].min().date()} to {df['Order Date'].max().date()}")
print("\nSample data:")
print(df.head())

# Create a figure with subplots
plt.figure(figsize=(15, 20))

# 1. Sales by Category
plt.subplot(3, 2, 1)
category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
plt.bar(category_sales.index, category_sales.values, color='skyblue')
plt.title('Sales by Category')
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)

# 2. Profit by Category
plt.subplot(3, 2, 2)
category_profit = df.groupby('Category')['Profit'].sum().sort_values(ascending=False)
plt.bar(category_profit.index, category_profit.values, color='lightgreen')
plt.title('Profit by Category')
plt.xlabel('Category')
plt.ylabel('Total Profit')
plt.xticks(rotation=45)

# 3. Sales by Region
plt.subplot(3, 2, 3)
region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
plt.bar(region_sales.index, region_sales.values, color='coral')
plt.title('Sales by Region')
plt.xlabel('Region')
plt.ylabel('Total Sales')

# 4. Sales vs Profit Scatter Plot
plt.subplot(3, 2, 4)
plt.scatter(df['Sales'], df['Profit'], alpha=0.5, color='purple')
plt.title('Sales vs. Profit')
plt.xlabel('Sales')
plt.ylabel('Profit')

# 5. Monthly Sales Trend
plt.subplot(3, 2, 5)
df['Month'] = df['Order Date'].dt.to_period('M')
monthly_sales = df.groupby('Month')['Sales'].sum()
monthly_sales.index = monthly_sales.index.to_timestamp()
plt.plot(monthly_sales.index, monthly_sales.values, marker='o', linestyle='-', color='blue')
plt.title('Monthly Sales Trend')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# 6. Top 10 Sub-Categories by Profit
plt.subplot(3, 2, 6)
subcategory_profit = df.groupby('Sub-Category')['Profit'].sum().sort_values(ascending=False)[:10]
plt.barh(subcategory_profit.index, subcategory_profit.values, color='teal')
plt.title('Top 10 Sub-Categories by Profit')
plt.xlabel('Total Profit')
plt.ylabel('Sub-Category')

# Adjust layout
plt.tight_layout()
plt.savefig('superstore_analysis.png')
plt.show()

# Create additional visualizations

# 7. Customer Segment Analysis
plt.figure(figsize=(15, 10))

# 7.1 Sales by Segment
plt.subplot(2, 2, 1)
segment_sales = df.groupby('Segment')['Sales'].sum().sort_values(ascending=False)
plt.bar(segment_sales.index, segment_sales.values, color='lightblue')
plt.title('Sales by Customer Segment')
plt.xlabel('Segment')
plt.ylabel('Total Sales')

# 7.2 Profit by Segment
plt.subplot(2, 2, 2)
segment_profit = df.groupby('Segment')['Profit'].sum().sort_values(ascending=False)
plt.bar(segment_profit.index, segment_profit.values, color='lightgreen')
plt.title('Profit by Customer Segment')
plt.xlabel('Segment')
plt.ylabel('Total Profit')

# 7.3 Quantity by Category
plt.subplot(2, 2, 3)
category_quantity = df.groupby('Category')['Quantity'].sum().sort_values(ascending=False)
plt.bar(category_quantity.index, category_quantity.values, color='orange')
plt.title('Quantity Sold by Category')
plt.xlabel('Category')
plt.ylabel('Total Quantity')

# 7.4 Distribution of Sales
plt.subplot(2, 2, 4)
plt.hist(df['Sales'], bins=50, alpha=0.75, color='gray')
plt.axvline(df['Sales'].mean(), color='r', linestyle='dashed', linewidth=2, label=f'Mean: {df["Sales"].mean():.2f}')
plt.title('Distribution of Sales')
plt.xlabel('Sales Value')
plt.ylabel('Frequency')
plt.legend()

plt.tight_layout()
plt.savefig('superstore_segment_analysis.png')
plt.show()

# 8. Ship Mode and Order Priority Analysis
plt.figure(figsize=(12, 6))

# 8.1 Sales by Ship Mode
plt.subplot(1, 2, 1)
ship_mode_sales = df.groupby('Ship Mode')['Sales'].sum().sort_values(ascending=False)
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
plt.pie(ship_mode_sales.values, labels=ship_mode_sales.index, autopct='%1.1f%%', 
        startangle=90, shadow=True, colors=colors, explode=[0.1, 0, 0, 0])
plt.title('Sales by Ship Mode')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

# 8.2 Average Ship Time (days between order and ship)
plt.subplot(1, 2, 2)
df['Ship Time (Days)'] = (df['Ship Date'] - df['Order Date']).dt.days
avg_ship_time = df.groupby('Ship Mode')['Ship Time (Days)'].mean().sort_values()
plt.bar(avg_ship_time.index, avg_ship_time.values, color='#66b3ff')
plt.title('Average Ship Time by Ship Mode')
plt.xlabel('Ship Mode')
plt.ylabel('Average Days')
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('superstore_shipping_analysis.png')
plt.show()

# 9. Sales and Profit over time
plt.figure(figsize=(14, 8))
df_time = df.set_index('Order Date')
monthly_metrics = df_time.resample('M')[['Sales', 'Profit']].sum()

# Create a two-line plot
fig, ax1 = plt.subplots(figsize=(14, 7))

# Plot Sales on primary y-axis
color = 'tab:blue'
ax1.set_xlabel('Date')
ax1.set_ylabel('Sales', color=color)
ax1.plot(monthly_metrics.index, monthly_metrics['Sales'], color=color, marker='o', linestyle='-')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_title('Monthly Sales and Profit Over Time')

# Create second y-axis for Profit
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Profit', color=color)
ax2.plot(monthly_metrics.index, monthly_metrics['Profit'], color=color, marker='s', linestyle='-')
ax2.tick_params(axis='y', labelcolor=color)

# Format x-axis to show dates properly
plt.gcf().autofmt_xdate()
plt.savefig('sales_profit_time_series.png')
plt.show()

print("\nAnalysis complete. Visualization images saved.")