"""Generate SYNTHETIC sample data, charts and sample reports for the portfolio.
All values are randomly generated (seed fixed) and do not come from any real company."""
import numpy as np, pandas as pd, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(2025)
ROOT = r"C:\hn\portfolio\projects"
RET = os.path.join(ROOT, "retail-store-performance-powerbi")
CAR = os.path.join(ROOT, "car-rental-overview-powerbi")
for p in (RET, CAR):
    for sub in ("data", "images", "reports"):
        os.makedirs(os.path.join(p, sub), exist_ok=True)

months = pd.period_range("2025-01", "2025-12", freq="M")
cal = pd.DataFrame({"date": pd.date_range("2025-01-01", "2025-12-31")})
cal["year"] = cal.date.dt.year; cal["quarter"] = cal.date.dt.quarter
cal["month"] = cal.date.dt.month; cal["month_name"] = cal.date.dt.strftime("%B")
cal["day"] = cal.date.dt.day; cal["weekday"] = cal.date.dt.strftime("%a")
cal.to_csv(os.path.join(RET, "data", "calendar.csv"), index=False)
cal.to_csv(os.path.join(CAR, "data", "calendar.csv"), index=False)

C = {"main": "#FF5500", "green": "#1F9E32", "blue": "#41a4ff", "grey": "#888888", "red": "#D34803"}
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
def money(x, pos=None): return f"{x/1000:,.0f}K"
def note(fig): fig.text(0.99, 0.005, "Synthetic sample data - illustrative preview", ha="right", fontsize=7, color="#888")

# ============================ RETAIL STORE PERFORMANCE ============================
stores = pd.DataFrame({"store_id": ["S1", "S2", "S3", "S4"],
                       "store_name": ["Store 1 - District 1", "Store 2 - District 3", "Store 3 - District 7", "Store 4 - Thu Duc"],
                       "size_factor": [1.3, 1.0, 0.9, 0.7]})
stores.to_csv(os.path.join(RET, "data", "stores.csv"), index=False)
promos = pd.DataFrame({"promotion_name": ["None", "BOGO", "B2G2", "B3G1", "B3G2", "B3G3", "B4G4"],
                       "description": ["No promotion", "Buy 1 get 1", "Buy 2 get 2", "Buy 3 get 1", "Buy 3 get 2", "Buy 3 get 3", "Buy 4 get 4"],
                       "free_share": [0, .5, .5, .25, .4, .5, .5]})
promos.to_csv(os.path.join(RET, "data", "promotions.csv"), index=False)
staff = [f"Staff {i:02d}" for i in range(1, 6)]
tiers = {"Luxury": (3_200_000, 0.15), "Premium": (1_500_000, 0.35), "Standard": (600_000, 0.50)}

rows = []; oid = 1
season = {1: 1.15, 2: .9, 3: .95, 4: 1.0, 5: 1.0, 6: 1.05, 7: 1.0, 8: 1.1, 9: 1.1, 10: 1.0, 11: 1.2, 12: 1.3}
for d in cal.date:
    for _, s in stores.iterrows():
        n = rng.poisson(5 * s.size_factor * season[d.month] * (1.25 if d.weekday() >= 5 else 1) * (1 + 0.02 * d.month))
        for _ in range(n):
            tier = rng.choice(list(tiers), p=[t[1] for t in tiers.values()])
            base = tiers[tier][0] * rng.uniform(.8, 1.2)
            promo = rng.choice(promos.promotion_name, p=[.55, .1, .08, .08, .07, .06, .06])
            share = float(promos.loc[promos.promotion_name == promo, "free_share"].iloc[0])
            amount = round(base * (1 - share * rng.uniform(.5, 1)) / 1000) * 1000
            rows.append((oid, d.date(), s.store_id, tier, promo, amount, round(base * share * 0.4 / 1000) * 1000 if promo != "None" else 0,
                         round(amount * rng.uniform(.38, .46) / 1000) * 1000, rng.choice(staff)))
            oid += 1
rev = pd.DataFrame(rows, columns=["order_id", "date", "store_id", "product_tier", "promotion_name", "amount_vnd", "promo_expense_vnd", "cogs_vnd", "sales_staff"])
rev.to_csv(os.path.join(RET, "data", "daily_revenue.csv"), index=False)
rev["date"] = pd.to_datetime(rev.date); rev["m"] = rev.date.dt.month

exp_rows = []
for m in range(1, 13):
    for _, s in stores.iterrows():
        sub = rev[(rev.m == m) & (rev.store_id == s.store_id)]
        sales = sub.amount_vnd.sum()
        exp_rows += [(m, s.store_id, "COG", sub.cogs_vnd.sum()),
                     (m, s.store_id, "Promo", sub.promo_expense_vnd.sum()),
                     (m, s.store_id, "Back Office", round(sales * rng.uniform(.06, .09))),
                     (m, s.store_id, "MKT", round(sales * rng.uniform(.04, .08))),
                     (m, s.store_id, "Warehouse", round(sales * rng.uniform(.02, .035))),
                     (m, s.store_id, "Cash Loss", round(sales * rng.uniform(0, .008))),
                     (m, s.store_id, "Sales Salary", round(sales * rng.uniform(.05, .07))),
                     (m, s.store_id, "Worker Salary", 18_000_000 + int(rng.integers(0, 4)) * 1_000_000)]
exp = pd.DataFrame(exp_rows, columns=["month", "store_id", "category", "amount_vnd"])
exp.to_csv(os.path.join(RET, "data", "expenses.csv"), index=False)

kpi = []
for m in range(1, 13):
    sub = rev[rev.m == m]
    for st in staff:
        made = sub[sub.sales_staff == st].amount_vnd.sum()
        target = 200_000_000
        kpi.append((m, st, made, target, round(made / target, 3), round(max(0, made - target) * 0.02), 8_000_000))
kpi = pd.DataFrame(kpi, columns=["month", "staff", "total_made_vnd", "kpi_target_vnd", "kpi_achievement", "bonus_vnd", "base_salary_vnd"])
kpi["total_salary_vnd"] = kpi.base_salary_vnd + kpi.bonus_vnd
kpi.to_csv(os.path.join(RET, "data", "staff_kpi.csv"), index=False)

m_sales = rev.groupby("m").amount_vnd.sum()
m_exp = exp.groupby("month").amount_vnd.sum()
m_profit = m_sales - m_exp
mn = [p.strftime("%b") for p in months]

# retail charts
fig, ax = plt.subplots(1, 3, figsize=(14, 3.6)); fig.suptitle("Retail Store Performance - Overview", fontweight="bold")
ax[0].plot(mn, m_sales / 1e6, color=C["main"], marker="o", label="Sales"); ax[0].plot(mn, m_exp / 1e6, color=C["grey"], marker="o", label="Expenses")
ax[0].set_title("Sales vs Expenses (M VND)"); ax[0].legend(frameon=False)
ax[1].bar(mn, m_profit / 1e6, color=[C["green"] if v >= 0 else C["red"] for v in m_profit]); ax[1].set_title("Profit by month (M VND)")
mom = m_sales.pct_change() * 100
ax[2].bar(mn[1:], mom.iloc[1:], color=[C["green"] if v >= 0 else C["red"] for v in mom.iloc[1:]]); ax[2].set_title("Sales MoM %"); ax[2].axhline(0, color="#333", lw=.6)
plt.setp(ax, xlabel=""); [a.tick_params(axis="x", rotation=45) for a in ax]; note(fig); fig.tight_layout(); fig.savefig(os.path.join(RET, "images", "01-overview.png"), dpi=130); plt.close(fig)

fig, ax = plt.subplots(1, 3, figsize=(14, 3.8)); fig.suptitle("Retail Store Performance - Expenses, Product mix & Promotions", fontweight="bold")
cat = exp.groupby("category").amount_vnd.sum().sort_values(ascending=False)
ax[0].pie(cat, labels=cat.index, autopct="%1.0f%%", startangle=90, wedgeprops=dict(width=.45), textprops={"fontsize": 7}); ax[0].set_title("Expenses by category")
tier = rev.groupby("product_tier").amount_vnd.sum()
ax[1].pie(tier, labels=tier.index, autopct="%1.0f%%", startangle=90, wedgeprops=dict(width=.45), colors=[C["main"], C["blue"], C["grey"]]); ax[1].set_title("Sales by product tier")
pr = rev[rev.promotion_name != "None"].groupby("promotion_name").amount_vnd.sum().sort_values()
ax[2].barh(pr.index, pr / 1e6, color=C["main"]); ax[2].set_title("Sales by promotion (M VND)")
note(fig); fig.tight_layout(); fig.savefig(os.path.join(RET, "images", "02-expenses-promotions.png"), dpi=130); plt.close(fig)

fig, ax = plt.subplots(1, 2, figsize=(14, 3.6)); fig.suptitle("Retail Store Performance - Staff KPI & Stores", fontweight="bold")
piv = kpi.pivot(index="month", columns="staff", values="total_made_vnd") / 1e6
piv.plot(kind="bar", ax=ax[0], width=.85); ax[0].axhline(200, color="#333", ls="--", lw=.8); ax[0].set_title("Total made by staff vs KPI target (M VND)"); ax[0].legend(frameon=False, ncol=5, fontsize=7); ax[0].set_xticklabels(mn, rotation=45)
ss = rev.merge(stores, on="store_id").groupby("store_name").amount_vnd.sum().sort_values()
ax[1].barh(ss.index, ss / 1e6, color=C["main"]); ax[1].set_title("Annual sales by store (M VND)")
note(fig); fig.tight_layout(); fig.savefig(os.path.join(RET, "images", "03-staff-stores.png"), dpi=130); plt.close(fig)

best = m_sales.idxmax(); worst = m_sales.idxmin()
top_promo = pr.idxmax(); top_store = ss.idxmax()
cogp = cat["COG"] / m_sales.sum()
open(os.path.join(RET, "reports", "sample-annual-report-2025.md"), "w", encoding="utf-8").write(f"""# Sample Annual Performance Report - 2025 (synthetic data)

> Generated from randomly simulated data in [`../data`](../data). Figures illustrate the report format and the analysis approach, not real business results.

| KPI | Value |
|---|---|
| Total sales | {m_sales.sum()/1e6:,.0f} M VND |
| Total expenses | {m_exp.sum()/1e6:,.0f} M VND |
| Profit | {m_profit.sum()/1e6:,.0f} M VND |
| Profit margin | {m_profit.sum()/m_sales.sum():.1%} |
| Orders | {len(rev):,} |
| Average order value | {rev.amount_vnd.mean()/1e3:,.0f} K VND |

## Highlights
- Peak month: **{mn[best-1]}** ({m_sales[best]/1e6:,.0f} M VND); weakest month: **{mn[worst-1]}** ({m_sales[worst]/1e6:,.0f} M VND). Sales are seasonal, rising toward year-end.
- COG is the largest cost block at {cogp:.0%} of sales; promotions cost {cat['Promo']/m_sales.sum():.1%} of sales.
- Best performing promotion by sales: **{top_promo}**. Best store: **{top_store}**.
- {int((kpi.kpi_achievement>=1).sum())} of {len(kpi)} staff-months reached the KPI target.

## Recommended actions (example format)
1. Review promotion mix: compare sales lift against promo expense per promotion before extending budgets.
2. Prepare inventory and staffing earlier for the Nov-Dec peak.
3. Track cash-loss lines monthly per store to find outliers early.
""")

# ============================ CAR RENTAL OVERVIEW ============================
makes = ["Toyota", "Mazda", "Hyundai", "Kia", "Honda", "MG", "Nissan"]
status_p = {"Active": .55, "RTO": .12, "Holding": .08, "Fixing": .08, "Sold": .09, "Lost": .02, "Inactive": .06}
N = 60
plates = [f"CAR-{i:03d}" for i in range(1, N + 1)]
car = pd.DataFrame({"plate": plates, "make": rng.choice(makes, N), "buying_price_aud": rng.integers(8, 28, N) * 1000,
                    "status": rng.choice(list(status_p), N, p=list(status_p.values()))})
car.to_csv(os.path.join(CAR, "data", "car_info.csv"), index=False)
cust = pd.DataFrame({"plate": plates, "customer_id": [f"CUST-{i:03d}" for i in range(1, N + 1)], "weekly_rate_aud": rng.integers(18, 34, N) * 10})
cust = cust.merge(car[["plate", "status"]], on="plate"); cust.to_csv(os.path.join(CAR, "data", "customers.csv"), index=False)

wk = pd.date_range("2025-01-06", "2025-12-29", freq="7D"); rows = []
for w in wk:
    for _, c in cust.iterrows():
        if c.status in ("Active", "RTO") and rng.random() < .9:
            rows.append((w.date(), c.plate, c.weekly_rate_aud, int(rng.random() < .04), 1, int(rng.random() < .03)))
rw = pd.DataFrame(rows, columns=["week_start", "plate", "amount_aud", "new_rent", "rented", "returned"])
rw.to_csv(os.path.join(CAR, "data", "revenue_weekly.csv"), index=False); rw["m"] = pd.to_datetime(rw.week_start).dt.month

mat_cats = ["Parts", "Others", "Rego", "GPS", "Tax", "Super"]
mrows = []
for m in range(1, 13):
    for _ in range(int(rng.integers(25, 45))):
        c = rng.choice(mat_cats, p=[.4, .15, .15, .1, .1, .1])
        mrows.append((m, rng.choice(plates), c, int(rng.integers(40, 900)), rng.choice(["Operation", "Invest"], p=[.7, .3])))
mat = pd.DataFrame(mrows, columns=["month", "plate", "category", "expense_aud", "type"]); mat.to_csv(os.path.join(CAR, "data", "expenses_material.csv"), index=False)
hr = pd.DataFrame([(m, f"Employee {i}", 3200 + 250 * i) for m in range(1, 13) for i in range(1, 4)], columns=["month", "employee", "total_aud"])
hr.to_csv(os.path.join(CAR, "data", "expenses_hr.csv"), index=False)
off = pd.DataFrame([(m, c, int(v * rng.uniform(.9, 1.1))) for m in range(1, 13) for c, v in [("Rent", 2500), ("MKT", 600), ("Utilities", 350), ("Software", 250)]], columns=["month", "category", "total_aud"])
off.to_csv(os.path.join(CAR, "data", "expenses_office.csv"), index=False)
debt = cust[cust.status.isin(["Active", "RTO"])].sample(frac=.25, random_state=1)[["customer_id", "plate"]].copy()
debt["outstanding_aud"] = rng.integers(1, 6, len(debt)) * 150; debt.to_csv(os.path.join(CAR, "data", "customer_debt.csv"), index=False)

r_rev = rw.groupby("m").amount_aud.sum()
r_mat = mat.groupby("month").expense_aud.sum(); r_hr = hr.groupby("month").total_aud.sum(); r_off = off.groupby("month").total_aud.sum()
r_exp = r_mat + r_hr + r_off; r_profit = r_rev - r_exp

fig, ax = plt.subplots(1, 3, figsize=(14, 3.6)); fig.suptitle("Car Rental - Overview", fontweight="bold")
ax[0].plot(mn, r_rev / 1e3, color=C["green"], marker="o", label="Revenue"); ax[0].plot(mn, r_exp / 1e3, color=C["red"], marker="o", label="Expenses"); ax[0].set_title("Revenue vs Expenses (K AUD)"); ax[0].legend(frameon=False)
ax[1].bar(mn, r_profit / 1e3, color=[C["green"] if v >= 0 else C["red"] for v in r_profit]); ax[1].set_title("Profit by month (K AUD)")
cs = car.status.value_counts(); ax[2].pie(cs, labels=cs.index, autopct="%1.0f%%", startangle=90, wedgeprops=dict(width=.45), textprops={"fontsize": 7}); ax[2].set_title("Cars by status")
[a.tick_params(axis="x", rotation=45) for a in ax[:2]]; note(fig); fig.tight_layout(); fig.savefig(os.path.join(CAR, "images", "01-overview.png"), dpi=130); plt.close(fig)

fig, ax = plt.subplots(1, 3, figsize=(14, 3.8)); fig.suptitle("Car Rental - Expense breakdown", fontweight="bold")
ec = pd.concat([mat.groupby("category").expense_aud.sum(), pd.Series({"HR": r_hr.sum(), "Office": r_off.sum()})]).sort_values(ascending=False)
ax[0].pie(ec, labels=ec.index, autopct="%1.0f%%", startangle=90, wedgeprops=dict(width=.45), textprops={"fontsize": 7}); ax[0].set_title("Total expenses by category")
t = mat.groupby("type").expense_aud.sum(); ax[1].bar(t.index, t, color=[C["blue"], C["main"]]); ax[1].set_title("Material: Operation vs Invest (AUD)")
oc = off.groupby("category").total_aud.sum().sort_values(); ax[2].barh(oc.index, oc, color=C["grey"]); ax[2].set_title("Office expenses (AUD)")
note(fig); fig.tight_layout(); fig.savefig(os.path.join(CAR, "images", "02-expenses.png"), dpi=130); plt.close(fig)

per = rw.groupby("plate").amount_aud.sum().rename("revenue"); mexp = mat.groupby("plate").expense_aud.sum().rename("expense")
cd = car.set_index("plate").join(per).join(mexp).fillna(0); cd["profit"] = cd.revenue - cd.expense
top = cd.sort_values("profit", ascending=False).head(10)
fig, ax = plt.subplots(1, 2, figsize=(14, 3.6)); fig.suptitle("Car Rental - Car detail", fontweight="bold")
ax[0].barh(top.index[::-1], top.profit[::-1] / 1e3, color=C["green"]); ax[0].set_title("Top 10 cars by profit (K AUD)")
wr = rw.groupby("week_start")[["new_rent", "returned"]].sum().rolling(4).sum(); ax[1].plot(range(len(wr)), wr.new_rent, label="New rent", color=C["green"]); ax[1].plot(range(len(wr)), wr.returned, label="Returned", color=C["red"]); ax[1].legend(frameon=False); ax[1].set_title("New rentals vs returns (rolling 4 weeks)")
note(fig); fig.tight_layout(); fig.savefig(os.path.join(CAR, "images", "03-car-detail.png"), dpi=130); plt.close(fig)

open(os.path.join(CAR, "reports", "sample-annual-report-2025.md"), "w", encoding="utf-8").write(f"""# Sample Annual Performance Report - 2025 (synthetic data)

> Generated from randomly simulated data in [`../data`](../data). Figures illustrate the report format and analysis approach, not real business results.

| KPI | Value |
|---|---|
| Total revenue | {r_rev.sum():,.0f} AUD |
| Total expenses | {r_exp.sum():,.0f} AUD |
| Profit | {r_profit.sum():,.0f} AUD |
| Profit margin | {r_profit.sum()/r_rev.sum():.1%} |
| Fleet size | {N} cars ({(car.status=='Active').sum()} Active, {(car.status=='RTO').sum()} RTO) |
| Customers with outstanding balance | {len(debt)} ({debt.outstanding_aud.sum():,.0f} AUD) |

## Highlights
- Highest revenue month: **{mn[r_rev.idxmax()-1]}**; lowest profit month: **{mn[r_profit.idxmin()-1]}**.
- Largest expense group: **{ec.index[0]}** ({ec.iloc[0]/r_exp.sum():.0%} of expenses).
- Best car: **{top.index[0]}** ({top.profit.iloc[0]:,.0f} AUD profit); {int((cd.profit<0).sum())} cars have not yet covered their material expenses.

## Recommended actions (example format)
1. Follow up customers with outstanding balances weekly to protect cash flow.
2. Review cars with negative profit: repair vs sell decision.
3. Separate Operation and Invest expenses in budget reviews to see true running cost.
""")
print("done", len(rev), len(rw))
print(m_sales.sum() / 1e6, m_profit.sum() / 1e6, r_rev.sum(), r_profit.sum())
