# PayTM — Customer Purchasing Trends Analysis

**Tools:** SQL (T-SQL / SQL Server), Excel
**Query file:** [`sql/paytm_analysis.sql`](sql/paytm_analysis.sql) · **Original repo:** [Project-PAYTM](https://github.com/hongnganguyen/Project-PAYTM)

## Business context
PayTM is a payment app. The goal is to understand customer purchasing habits, find the most popular products, judge whether promotions work, and identify valuable customer groups across the 12 months of 2018.

## Data
| Table | Description |
|---|---|
| `payment_history_18` | Orders: customer, product, promotion (`promotion_id = 0` means none), bank, platform, discount/final price, transaction date |
| `product` | Category, sub-category, product group, online/offline |
| `paying_method` | Payment method lookup |
| `table_message` | Payment notification / status per order |

Small lookup tables are in [`data/`](data). The full `payment_history_18.csv` (~22 MB) stays in the [original repo](https://github.com/hongnganguyen/Project-PAYTM/tree/main/SQL%20-%20Project%20PayTM/Dataset).

## Analysis
1. **Top products** — transaction count by customer, category and sub-category.
2. **Promotion overview** — share of successful Telco transactions that used a promotion, by month.
3. **Promotion effectiveness** — customers whose first purchase used a promotion and who then made a normal (non-promo) repeat purchase.
4. **Cohort analysis** — monthly retention of Telco customers over 2018 (CTEs, window functions, `PIVOT`).
5. **RFM segmentation** — Recency / Frequency / Monetary scored with `PERCENT_RANK`, grouped into segments (Best, Loyal, Big Spenders, Potential Loyalists, Almost Lost, Lost, Hibernating, New).

## Key findings
- Telco is the most purchased product category, so it deserves dedicated promotions and attention.
- The promotion program's share of successful transactions rose gradually, peaking in August and November, then declined.
- Repeat purchases after a first promotional transaction exceeded 50% of the customers measured, showing promotions are effective at acquiring customers who come back.
- Cohort and RFM views give a 12-month picture of the Telco customer segments for targeted campaigns.

## SQL techniques
Multi-table JOINs · CTEs · window functions (`LAG`, `ROW_NUMBER`, `PERCENT_RANK`) · `PIVOT` · temp tables · conditional segmentation with `CASE`.
