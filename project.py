import pandas as pd
import matplotlib.pyplot as plt

# 1. Load your CSV file
file_name = '/nifty_data.csv'
df = pd.read_csv(file_name)

print("--- Initial Data Preview ---")
print(df.head()) # Shows us what columns were loaded

# 2. Clean the columns: Assume first column is Date, clean the rest
date_col = df.columns[0]
df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
df.dropna(subset=[date_col], inplace=True)
df.set_index(date_col, inplace=True)

# Clean all numeric columns (removes commas if any, converts text to numbers)
for col in df.columns:
    if df[col].dtype == object:
        df[col] = df[col].astype(str).str.replace(',', '').str.strip()
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop rows with any remaining missing data
df.dropna(inplace=True)

print(f"Total rows loaded successfully: {len(df)}")

# 3. Normalize data to 100 for a fair comparison starting point (Line Chart prep)
df_normalized = (df / df.iloc[0]) * 100

# --- CHART 1: LINE CHART (2-Year Performance Trend vs Nifty 50) ---
plt.figure(figsize=(10, 5))
for column in df_normalized.columns:
    plt.plot(df_normalized.index, df_normalized[column], label=column, linewidth=2)
plt.title('2-Year Sectoral Performance vs Nifty 50 (Base = 100)')
plt.xlabel('Date')
plt.ylabel('Normalized Growth (Start = 100)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# Calculate total 2-year return percentage for bar and pie charts
total_returns = ((df.iloc[-1] - df.iloc[0]) / df.iloc[0]) * 100

# --- CHART 2: BAR GRAPH (Total 2-Year Return Comparison) ---
plt.figure(figsize=(9, 4))
colors = ['green' if x > 0 else 'red' for x in total_returns]
total_returns.plot(kind='bar', color=colors, edgecolor='black')
plt.title('Total 2-Year Return (%) by Sector')
plt.ylabel('Return (%)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.show()

# --- CHART 3: PIE CHART (Proportional Share of Positive Returns) ---
positive_returns = total_returns[total_returns > 0]

plt.figure(figsize=(6, 6))
plt.pie(positive_returns, labels=positive_returns.index, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
plt.title('Share of Outperformance Among Positive Sectors')
plt.show()
