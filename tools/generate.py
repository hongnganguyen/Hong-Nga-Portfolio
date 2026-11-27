"""Generate SYNTHETIC sample data and sample reports for the two Power BI portfolio projects.
Project 1: car rental SALES performance (rentals, promotions, customers, costs, team).
Project 2: car rental OVERVIEW (fleet, expenses by group, Operation vs Invest, customer debt).
All values are randomly generated (fixed seed). They do not come from any real company, customer or employee.
Usage: python tools/generate.py   (then: python tools/build_dashboard.py)"""
import os
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "projects")
SAL = os.path.join(ROOT, "car-rental-sales-performance-powerbi")
CAR = os.path.join(ROOT, "car-rental-overview-powerbi")
for p in (SAL, CAR):
    for sub in ("data", "images", "reports"):
        os.makedirs(os.path.join(p, sub), exist_ok=True)

days = pd.date_range("2025-01-01", "2025-12-31")
cal = pd.DataFrame({"date": days.date, "year": days.year, "quarter": days.quarter, "month": days.month,
                    "month_name": days.strftime("%B"), "day": days.day, "weekday": days.strftime("%a")})
cal.to_csv(os.path.join(SAL, "data", "calendar.csv"), index=False)
cal.to_csv(os.path.join(CAR, "data", "calendar.csv"), index=False)
MN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
dim = {m: int(pd.Period(f"2025-{m:02d}").days_in_month) for m in range(1, 13)}

# =============================== PROJECT 1: CAR RENTAL SALES PERFORMANCE (AUD) ===============================
suburbs = [("Parramatta", -33.815, 151.001, 9), ("Bankstown", -33.917, 151.035, 8), ("Chatswood", -33.797, 151.180, 6),
           ("Sutherland", -34.031, 151.057, 5), ("Liverpool", -33.920, 150.923, 7), ("Blacktown", -33.771, 150.906, 7),
           ("Manly", -33.797, 151.287, 3), ("Bondi", -33.891, 151.274, 3), ("Hornsby", -33.704, 151.099, 4),
           ("Randwick", -33.914, 151.242, 4), ("Burwood", -33.877, 151.104, 6), ("Fairfield", -33.872, 150.956, 6),
           ("Auburn", -33.849, 151.033, 6), ("Strathfield", -33.873, 151.094, 5), ("Campbelltown", -34.065, 150.814, 3),
           ("Penrith", -33.751, 150.694, 3), ("Hurstville", -33.967, 151.100, 5), ("Ryde", -33.815, 151.105, 5),
           ("Marrickville", -33.911, 151.155, 5), ("Mascot", -33.929, 151.193, 4)]
sub_df = pd.DataFrame(suburbs, columns=["suburb", "lat", "lon", "weight"])
sub_df.to_csv(os.path.join(SAL, "data", "suburbs.csv"), index=False)
sub_p = (sub_df.weight / sub_df.weight.sum()).values

promo_tbl = pd.DataFrame({"promotion_name": ["None", "BOGO", "BSGM", "B4G4", "B3G2", "B2G2", "IM"],
                          "description": ["No promotion", "Free-day promotion (BOGO)", "Free-day promotion (BSGM)", "Free-day promotion (B4G4)",
                                          "Free-day promotion (B3G2)", "Free-day promotion (B2G2)", "Introductory offer (IM)"],
                          "discount_rate": [0, .20, .12, .18, .14, .11, .06],
                          "probability": [.50, .20, .13, .07, .04, .04, .02]})
promo_tbl.to_csv(os.path.join(SAL, "data", "promotions.csv"), index=False)
staff = [f"Staff {c}" for c in "ABCDE"]
season = {1: .95, 2: .86, 3: 1.0, 4: .97, 5: 1.0, 6: 1.06, 7: 1.0, 8: 1.05, 9: 1.04, 10: 1.0, 11: 1.12, 12: 1.22}
dur_p = [.30, .28, .18, .10, .06, .05, .03]

rows, rid = [], 1
cust_home, cust_ids = {}, []
for d in days:
    n = rng.poisson(7.2 * season[d.month] * (1.18 if d.dayofweek >= 5 else 1.0) * (1 + 0.0006 * d.dayofyear))
    repeat_p = 0.12 + 0.20 * d.dayofyear / 365
    for _ in range(n):
        if cust_ids and rng.random() < repeat_p:
            cid = cust_ids[int(rng.integers(len(cust_ids)))]; is_new = 0; sub = cust_home[cid]
        else:
            cid = f"CUST-{len(cust_ids) + 1:04d}"; sub = str(rng.choice(sub_df.suburb, p=sub_p)); cust_home[cid] = sub; cust_ids.append(cid); is_new = 1
        cls = str(rng.choice(["Premium", "Luxury"], p=[.58, .42]))
        rate = rng.uniform(55, 85) if cls == "Premium" else rng.uniform(95, 150)
        nd = int(rng.choice([1, 2, 3, 4, 5, 6, 7], p=dur_p))
        pr = promo_tbl.sample(1, weights=promo_tbl.probability, random_state=int(rng.integers(1e9))).iloc[0]
        listamt = rate * nd
        amount = round(listamt * (1 - pr.discount_rate), 2)
        promo_exp = round(listamt * pr.discount_rate * 0.6, 2) if pr.promotion_name != "None" else 0.0
        rows.append((rid, d.date(), sub, cid, is_new, cls, nd, amount, pr.promotion_name, promo_exp,
                     round(amount * rng.uniform(.30, .36), 2), str(rng.choice(staff))))
        rid += 1
rentals = pd.DataFrame(rows, columns=["rental_id", "date", "suburb", "customer_id", "is_new_customer", "car_class", "rental_days",
                                      "amount_aud", "promotion_name", "promo_cost_aud", "direct_cost_aud", "sales_staff"])
rentals.to_csv(os.path.join(SAL, "data", "rentals.csv"), index=False)
rentals["m"] = pd.to_datetime(rentals.date).dt.month

# staff KPI by month
kp = []
for m in range(1, 13):
    sub = rentals[rentals.m == m]
    for s in staff:
        made = round(sub[sub.sales_staff == s].amount_aud.sum(), 2)
        target = 10000.0
        commission = round(made * .04, 2)
        bonus = 150.0 if made >= target else 0.0
        kp.append((m, s, made, target, round(made / target, 3), 900.0, commission, bonus, round(900 + commission + bonus, 2)))
kpi = pd.DataFrame(kp, columns=["month", "staff", "total_made_aud", "kpi_target_aud", "kpi_achievement", "base_salary_aud",
                                "commission_aud", "bonus_aud", "total_salary_aud"])
kpi.to_csv(os.path.join(SAL, "data", "staff_kpi.csv"), index=False)

# daily expenses (category names are business names, not generic ledger codes)
er = []
by_day = rentals.groupby("date").agg(cost=("direct_cost_aud", "sum"), promo=("promo_cost_aud", "sum"))
sal_month = kpi.groupby("month").total_salary_aud.sum()
ops_month = {m: 11000 + float(rng.integers(-400, 500)) for m in range(1, 13)}
for d in days:
    m, k = d.month, dim[d.month]
    ds = d.date()
    er += [(ds, "Direct cost", round(by_day.cost.get(ds, 0.0), 2)), (ds, "Promo cost", round(by_day.promo.get(ds, 0.0), 2)),
           (ds, "Sales salary", round(sal_month[m] / k, 2)), (ds, "Ops staff salary", round(ops_month[m] / k, 2)),
           (ds, "Garage & yard", round(3200 / k, 2)), (ds, "Back office", round(1800 / k, 2))]
    if rng.random() < .30: er.append((ds, "Damage & loss", round(float(rng.uniform(60, 400)), 2)))
    if d.dayofweek == 0: er.append((ds, "Marketing", round(float(rng.uniform(120, 260)), 2)))
    if d.day == 1: er.append((ds, "Office", round(float(rng.uniform(60, 110)), 2)))
exp = pd.DataFrame(er, columns=["date", "category", "amount_aud"])
exp.to_csv(os.path.join(SAL, "data", "expenses.csv"), index=False)

# =============================== PROJECT 2: CAR RENTAL OVERVIEW (AUD) ===============================
makes = ["Toyota", "Mazda", "Hyundai", "Kia", "Honda", "MG", "Nissan"]
status_p = {"Active": .55, "RTO": .12, "Holding": .08, "Fixing": .08, "Sold": .09, "Lost": .02, "Inactive": .06}
N = 60
plates = [f"CAR-{i:03d}" for i in range(1, N + 1)]
car = pd.DataFrame({"plate": plates, "make": rng.choice(makes, N), "buying_price_aud": rng.integers(8, 28, N) * 1000,
                    "daily_rate_aud": rng.integers(24, 38, N), "status": rng.choice(list(status_p), N, p=list(status_p.values()))})
car.to_csv(os.path.join(CAR, "data", "car_info.csv"), index=False)

rev_rows, ev_rows = [], []
for _, c in car[car.status.isin(["Active", "RTO"])].iterrows():
    rented = rng.random() < .7
    for d in days:
        if rented:
            if rng.random() < .035:
                rented = False; ev_rows.append((d.date(), c.plate, "returned"))
        elif rng.random() < .08:
            rented = True; ev_rows.append((d.date(), c.plate, "new_rent"))
        if rented:
            rev_rows.append((d.date(), c.plate, float(c.daily_rate_aud)))
rev = pd.DataFrame(rev_rows, columns=["date", "plate", "amount_aud"]); rev.to_csv(os.path.join(CAR, "data", "revenue_daily.csv"), index=False)
ev = pd.DataFrame(ev_rows, columns=["date", "plate", "event"]); ev.to_csv(os.path.join(CAR, "data", "rental_events.csv"), index=False)

xr = []
rd = lambda m: pd.Timestamp(2025, m, int(rng.integers(1, dim[m] + 1))).date()
for pl in plates:  # registration: two slips per car per year
    for nm in ("Pinkslip", "Greenslip"):
        m = int(rng.integers(1, 13)); xr.append((rd(m), "Material", "Rego", pl, f"{nm}_{pl}", round(float(rng.uniform(640, 715)), 2), "Invest" if rng.random() < .2 else "Operation"))
for m in range(1, 13):
    for _ in range(int(rng.integers(8, 13))):
        pl = rng.choice(plates); item = rng.choice(["Tyres x2", "Battery", "Brake pads", "Wipers", "Service kit", "Headlight"])
        xr.append((rd(m), "Material", "Parts", pl, f"{item} - {pl}", round(float(rng.uniform(90, 420)), 2), "Invest" if rng.random() < .8 else "Operation"))
    for _ in range(int(rng.integers(20, 30))):
        item = rng.choice(["Toll", "Fuel", "Cleaning", "Parking", "Transfer fee", "Roadside help"])
        xr.append((rd(m), "Material", "Others", rng.choice(plates), f"{item} ({rd(m)})", round(float(rng.uniform(25, 520)), 2), "Invest" if rng.random() < .15 else "Operation"))
    for item, lo, hi in [("Electricity", 280, 360), ("SIM plans", 260, 340), ("Software subscription", 240, 330), ("Staff meals", 200, 300), ("Hotline", 120, 160)]:
        xr.append((rd(m), "Material", "Operation", "", item, round(float(rng.uniform(lo, hi)), 2), "Operation"))
    if m in (3, 6, 9, 12): xr.append((rd(m), "Material", "Tax", "", "Quarterly tax", round(float(rng.uniform(800, 1100)), 2), "Operation"))
    if m % 3 == 1: xr.append((rd(m), "Material", "Rent", "", "Yard rent", round(float(rng.uniform(900, 1300)), 2), "Operation"))
    for i, nm in enumerate(["Staff A", "Staff B", "Staff C"]):
        xr.append((pd.Timestamp(2025, m, 5).date(), "HR", "Salary", "", f"{nm} salary", round(float([2000, 1550, 800 + float(rng.integers(0, 400))][i]), 2), "Operation"))
    xr.append((pd.Timestamp(2025, m, 12).date(), "MKT", "Advertising", "", "Online advertising", round(float(rng.uniform(600, 900)), 2), "Operation"))
    xr.append((pd.Timestamp(2025, m, 1).date(), "Office", "Office", "", "Office expenses", round(float(rng.uniform(80, 220)), 2), "Operation"))
cexp = pd.DataFrame(xr, columns=["date", "group", "category", "plate", "note", "amount_aud", "type"]).sort_values("date")
cexp.to_csv(os.path.join(CAR, "data", "expenses.csv"), index=False)

debt = pd.DataFrame({"month": range(1, 13), "outstanding_aud": [round(float(rng.uniform(3200, 5200)), 2) for _ in range(12)],
                     "pct_customers_paid": [round(float(rng.uniform(.70, .88)), 3) for _ in range(12)]})
debt.to_csv(os.path.join(CAR, "data", "customer_debt.csv"), index=False)

# =============================== SAMPLE REPORTS ===============================
def pct(a, b): return f"{(a - b) / abs(b):+.1%}" if b else "n/a"
def aud(x): return f"{'-' if x < 0 else ''}A${abs(x):,.0f}"

M, P = 11, 10
dts = pd.to_datetime(exp.date)
rs = rentals.groupby("m").amount_aud.sum(); ex = exp.groupby(dts.dt.month).amount_aud.sum(); rp = rs - ex
cat_m = exp[dts.dt.month == M].groupby("category").amount_aud.sum().sort_values(ascending=False)
pm = rentals[rentals.m == M]
pp = pm[pm.promotion_name != "None"].groupby("promotion_name").agg(n=("rental_id", "count"), sales=("amount_aud", "sum"), pc=("promo_cost_aud", "sum"), dc=("direct_cost_aud", "sum"))
pp["profit"] = pp.sales - pp.dc - pp.pc
pp = pp.sort_values("sales", ascending=False)
no = pm[pm.promotion_name == "None"]
mg_no = (no.amount_aud.sum() - no.direct_cost_aud.sum()) / no.amount_aud.sum()
mg_pr = (pp.sales.sum() - pp.dc.sum() - pp.pc.sum()) / pp.sales.sum()
dprof = (pm.groupby("date").amount_aud.sum() - exp[dts.dt.month == M].groupby("date").amount_aud.sum()).dropna()
neg_days = int((dprof < 0).sum())
cu = pm.customer_id.nunique(); new_c = int(pm.is_new_customer.sum())
lines = "\n".join(f"| {k} | {int(r.n)} | {r.sales:,.0f} | {r.pc:,.0f} | {r.profit:,.0f} |" for k, r in pp.iterrows())
open(os.path.join(SAL, "reports", "sample-report-2025-11.md"), "w", encoding="utf-8").write(f"""# Sample monthly report - November 2025 (synthetic data)

> Generated from randomly simulated data in [`../data`](../data). The numbers illustrate the report format and the analysis approach; they are **not real business results**.

| KPI | Nov 2025 | vs Oct 2025 |
|---|---|---|
| Rental sales | {aud(rs[M])} | {pct(rs[M], rs[P])} |
| Total expenses | {aud(ex[M])} | {pct(ex[M], ex[P])} |
| Profit | {aud(rp[M])} | {pct(rp[M], rp[P])} |
| Profit margin | {rp[M]/rs[M]:.1%} | {rp[P]/rs[P]:.1%} |
| Rentals | {len(pm):,} | {(rentals.m==P).sum():,} |
| Average rental value | {aud(pm.amount_aud.mean())} | {pct(pm.amount_aud.mean(), rentals[rentals.m==P].amount_aud.mean())} |
| Unique customers | {cu:,} ({new_c:,} new) | |

## Expense structure (Nov)
{chr(10).join(f"- **{k}**: {aud(v)} ({v/ex[M]:.0%})" for k, v in cat_m.items())}

## Promotion performance (Nov)
| Promotion | Rentals | Sales (A$) | Promo cost (A$) | Profit after direct and promo cost (A$) |
|---|---|---|---|---|
{lines}

Margin after direct and promo cost: **{mg_pr:.1%}** on promotional rentals vs **{mg_no:.1%}** on full-price rentals.

## Highlights
- The month has **{neg_days} loss-making day(s)**; the best day earned {aud(dprof.max())} and the weakest {aud(dprof.min())}.
- **{pp.index[0]}** is the top promotion by sales ({pp.sales.iloc[0]/pm.amount_aud.sum():.0%} of the month); compare its promo cost with the profit it generates before extending it.
- Premium cars bring {pm[pm.car_class=='Premium'].amount_aud.sum()/pm.amount_aud.sum():.0%} of rental sales and Luxury {pm[pm.car_class=='Luxury'].amount_aud.sum()/pm.amount_aud.sum():.0%}.
- Staff salaries and garage costs are fixed, so profit is thin on low-rental days.

## Recommended actions (example format)
1. Concentrate promotions on low-demand days instead of days that already book well.
2. Review damage and loss events weekly to find recurring causes.
3. Grow the repeat-customer share with a loyalty offer in the top suburbs.
""")

rr = rev.assign(m=pd.to_datetime(rev.date).dt.month).groupby("m").amount_aud.sum()
cx = cexp.assign(m=pd.to_datetime(cexp.date).dt.month)
cxm = cx.groupby("m").amount_aud.sum(); cp = rr - cxm
grp = cx[cx.m == M].groupby("group").amount_aud.sum().sort_values(ascending=False)
mat = cx[(cx.m == M) & (cx.group == "Material")].groupby("category").amount_aud.sum().sort_values(ascending=False)
renting = rev[rev.date == pd.Timestamp(2025, M, 30).date()].plate.nunique()
open(os.path.join(CAR, "reports", "sample-report-2025-11.md"), "w", encoding="utf-8").write(f"""# Sample monthly report - November 2025 (synthetic data)

> Generated from randomly simulated data in [`../data`](../data). The numbers illustrate the report format and the analysis approach; they are **not real business results**.

| KPI | Nov 2025 | vs Oct 2025 |
|---|---|---|
| Total sales | {aud(rr[M])} | {pct(rr[M], rr[P])} |
| Total expenses | {aud(cxm[M])} | {pct(cxm[M], cxm[P])} |
| Profit | {aud(cp[M])} | {pct(cp[M], cp[P])} |
| Profit margin | {cp[M]/rr[M]:.1%} | {cp[P]/rr[P]:.1%} |
| Cars on rent (30 Nov) | {renting} of {int(car.status.isin(['Active','RTO']).sum())} rentable | |
| Outstanding customer balance | {aud(debt.outstanding_aud[M-1])} | {debt.pct_customers_paid[M-1]:.0%} customers paid |

## Expense structure (Nov)
{chr(10).join(f"- **{k}**: {aud(v)} ({v/cxm[M]:.0%})" for k, v in grp.items())}

Material expenses by category: {", ".join(f"{k} {aud(v)}" for k, v in mat.items())}.

## Highlights
- Registration (Rego) and parts are lumpy costs, so daily profit swings even when revenue is steady.
- Only {int(car.status.isin(['Active','RTO']).sum())} of {N} cars can earn rental income (Active / RTO); the rest are Holding, Fixing, Sold, Lost or Inactive.
- Material costs are split into **Operation** vs **Invest** so running costs are not mixed with fleet investment.

## Recommended actions (example format)
1. Follow up customers with outstanding balances weekly to protect cash flow.
2. Review Fixing / Holding cars: repair, rent out again or sell.
3. Schedule registration renewals in advance to smooth cash needs.
""")
print("done: rentals", len(rentals), "| fleet revenue rows", len(rev))
print("Nov sales/profit", round(rs[M]), round(rp[M]), "| fleet revenue/profit", round(rr[M]), round(cp[M]))
