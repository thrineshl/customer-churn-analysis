# Customer Churn Analysis
# Goal: Identify key factors driving customer churn
# Dataset: Telco Customer Churn (7043 records)
# Tools: Python, Pandas, SQLite, Matplotlib, Seaborn
-- Churn rate by contract type
SELECT Contract,
       COUNT(*) AS total,
       SUM(Churn) AS churned,
       ROUND(100.0 * SUM(Churn) / COUNT(*), 2) AS churn_rate
FROM customers
GROUP BY Contract
ORDER BY churn_rate DESC;

-- High-risk segment: month-to-month + high charges
SELECT customerID, tenure, MonthlyCharges, TotalCharges
FROM customers
WHERE Contract = 'Month-to-month'
  AND MonthlyCharges > 70
  AND Churn = 1;

-- Avg monthly charges: churned vs retained
SELECT Churn,
       ROUND(AVG(MonthlyCharges), 2) AS avg_monthly,
       ROUND(AVG(tenure), 2) AS avg_tenure
FROM customers
GROUP BY Churn;
