# Azuz Web — Customer Purchasing Behavior Analysis

**Tools:** SQL (T-SQL / SQL Server)
**Query file:** [`sql/azuz_analysis.sql`](sql/azuz_analysis.sql) · **Original repo:** [Project-Azuz-Web](https://github.com/hongnganguyen/Project-Azuz-Web)

## Business context
An in-depth look at how customers buy on the Azuz website: product preferences, purchase habits, the effect of gold membership, and how a points-based loyalty program could attract customers.

## Data ([`data/`](data))
`sales` (userid, created_date, product_id) · `product` (product_id, name, price) · `users` (userid, signup_date) · `goldusers_signup` (userid, gold_signup_date)

> This is a small teaching-scale dataset (3 customers, 16 orders). The value of the project is the analytical approach and SQL, not statistical significance.

## Analysis
1. **Behavior & patterns** — total spend per customer, visit frequency, first product bought, most-purchased product, favorite product per customer.
2. **Before vs. after gold membership** — first item after joining, last item before joining, orders and spend before joining.
3. **Loyalty program** — points per product (p1: $5 = 1 point, p2: $2 = 1 point, p3: $5 = 1 point; 2 points = $5 discount), which product earns the most points, and gold members' points in their first year.
4. **Transaction ranking** — rank every transaction, and flag gold-member transactions (non-gold marked `NA`).

## Key findings
- Product 1 is the most common first purchase among new customers, but purchases shift toward product 2 over time.
- Customer 1 buys product 2 consistently before and after joining; customer 3's behavior changes after joining.
- Product 2 earns the most loyalty points, so the points program is best aligned with it.
- Customer 3 raised spending in the first year of gold membership despite fewer total points, suggesting the gold tier is effective.

## SQL techniques
JOINs · CTEs · `RANK()` over partitions · subqueries · `CASE` · date functions (`DATEADD`) · conditional `LEFT JOIN`.
