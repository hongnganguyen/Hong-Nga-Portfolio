# Car Rental Overview Dashboard — Power BI

**Tools:** Power BI (data modeling, DAX, Power Query), Excel
**Currency:** AUD · **Period shown:** 2025 (synthetic)

> ⚠️ **About the data.** The original dashboard was built for a real employer, so its data (customers, plates, staff, finances) is confidential and is not published. All data in this folder is **synthetic**, randomly generated with the same table structure and the same kind of metrics as the real model. Charts below are *illustrative previews* made from synthetic data; they are not screenshots of the production report and the numbers are not real business results.

## Business problem
A car-rental operation needed to track revenue, every expense group, profit, fleet status and customer debt in one dashboard, and to see the profitability of each car.

## Dashboard structure (2 pages)
| Page | What it shows |
|---|---|
| **Car Rental (overview)** | Total sales, total orders, total expenses and profit with % of sales; revenue by type (Parts, Others, Rego, Operation, Rent, Tax); expenses split into **Invest** vs **Operation**, with Material, HR, Marketing and Office breakdowns; customer debt and % customers paid; sales & expenses and profit trendlines; year/quarter/month slicers; bookmarks to switch views (Rent / Automotive / Office / Material) |
| **Car Rental Detail** | Fleet by status (Active, RTO, Holding, Fixing, Sold, Lost, Inactive); per-car revenue, expenses and profit; buying price; customer and plate lookup; weekly new rentals vs. returns |

## Data model
`car_info` · `customers` · `revenue_weekly` · `expenses_material` · `expenses_hr` · `expenses_office` · `customer_debt` · `calendar`
CSV files in [`data/`](data) (60 synthetic cars, 52 weeks).

Measures in the model (names): Rent Total Sales / Expenses / Profit, Rent Material Exp, Rent HR Expenses, Rent MKT Expenses, Rent Exp for Invest / Operation, Rent Total Orders, % format vs Sales/Expenses/Profit, Total debt and % customers paid, Car_Detail Revenue / Expenses / Profit.

## Preview (synthetic data)
![Overview](images/01-overview.png)
![Expenses](images/02-expenses.png)
![Car detail](images/03-car-detail.png)

## Sample report
[`reports/sample-annual-report-2025.md`](reports/sample-annual-report-2025.md) — example periodic report (KPIs, highlights, recommended actions) computed from the synthetic data.

## How to reproduce
Load the CSVs into Power BI Desktop, relate `plate` across `car_info`, `customers`, `revenue_weekly` and `expenses_material`, link dates/months to `calendar`, then build the measures above. Generator: [`/tools/generate.py`](../../tools/generate.py).
