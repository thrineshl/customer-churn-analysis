import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- CONFIG ---
DATA_PATH = "data/churn_data.csv"
DB_PATH = "data/churn.db"
PLOT_DIR = "outputs/plots"
os.makedirs(PLOT_DIR, exist_ok=True)

# --- LOAD ---
df = pd.read_csv(DATA_PATH)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df.dropna(inplace=True)
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

# --- LOAD INTO SQLITE ---
conn = sqlite3.connect(DB_PATH)
df.to_sql("customers", conn, if_exists="replace", index=False)

# --- SQL ANALYSIS ---
queries = {
    "churn_by_contract": """
        SELECT Contract, COUNT(*) as total,
               SUM(Churn) as churned,
               ROUND(100.0 * SUM(Churn) / COUNT(*), 2) as churn_rate
        FROM customers
        GROUP BY Contract
    """,
    "avg_tenure_churned": """
        SELECT Churn, ROUND(AVG(tenure), 2) as avg_tenure
        FROM customers GROUP BY Churn
    """,
    "churn_by_service": """
        SELECT InternetService, ROUND(100.0*SUM(Churn)/COUNT(*),2) as churn_rate
        FROM customers GROUP BY InternetService
    """
}

for name, q in queries.items():
    print(f"\n=== {name} ===")
    print(pd.read_sql(q, conn).to_string(index=False))

# --- EDA PLOTS ---
# 1. Churn distribution
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

df['Churn'].value_counts().plot(kind='bar', ax=axes[0], color=['steelblue','tomato'])
axes[0].set_title('Churn Distribution')
axes[0].set_xticklabels(['No Churn', 'Churn'], rotation=0)

# 2. Tenure vs Churn
df.groupby('Churn')['tenure'].plot(kind='kde', ax=axes[1], legend=True)
axes[1].set_title('Tenure by Churn')
axes[1].legend(['No Churn', 'Churn'])

# 3. Contract type vs churn rate
contract_churn = pd.read_sql(queries['churn_by_contract'], conn)
axes[2].bar(contract_churn['Contract'], contract_churn['churn_rate'], color='coral')
axes[2].set_title('Churn Rate by Contract Type')
axes[2].set_ylabel('Churn Rate (%)')

plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/churn_overview.png", dpi=150)
plt.close()

# 4. Correlation heatmap
num_cols = df.select_dtypes(include='number')
plt.figure(figsize=(8, 6))
sns.heatmap(num_cols.corr(), annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/correlation.png", dpi=150)
plt.close()

conn.close()
print("\nDone. Plots saved to outputs/plots/")