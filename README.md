# Customer Churn Analysis

End-to-end EDA on telecom customer data to identify churn drivers and propose retention strategies.

## Tools
Python · Pandas · SQLite · Matplotlib · Seaborn · Jupyter

## Key Findings
- Month-to-month contracts show **42.71% churn** vs just 2.85% for two-year contracts
- Churned customers have avg tenure of **17.98 months** vs 37.65 months for retained
- Fiber optic users churn at **41.89%** vs DSL at 19%
- High monthly charges (>$70) + short tenure = highest risk segment

## Retention Strategies Proposed
1. Offer contract upgrade incentives at 3-month mark
2. Target fiber optic users with loyalty discounts
3. Flag customers: tenure <12mo + charges >$70 for proactive outreach

## Structure
data/ → raw CSV + SQLite DB  
sql/ → standalone SQL queries  
outputs/plots/ → saved visualizations