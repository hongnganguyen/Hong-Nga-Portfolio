"""Aggregate the SYNTHETIC CSVs into docs/data.js for the interactive dashboards.
Run after tools/generate.py:  python tools/build_dashboard.py"""
import os, json
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MFG = os.path.join(ROOT, "projects", "glass-manufacturing-performance-powerbi", "data")
CAR = os.path.join(ROOT, "projects", "car-rental-overview-powerbi", "data")
OUT = os.path.join(ROOT, "docs")
os.makedirs(OUT, exist_ok=True)
NA = dict(keep_default_na=False)  # "None" is a real promotion label, not a missing value


def rows(df):
    return json.loads(df.to_json(orient="values"))


# ---------------- project 1: glass manufacturing performance ----------------
o = pd.read_csv(os.path.join(MFG, "orders.csv"), **NA)
o["m"] = pd.to_datetime(o.date).dt.month
daily = (o.groupby(["date", "product_line", "promotion_name"])
         .agg(units=("quantity", "sum"), sales=("amount_aud", "sum"), promo=("promo_cost_aud", "sum"), cogs=("cogs_aud", "sum"),
              n=("order_id", "count"), newc=("is_new_customer", "sum"))
         .round(2).reset_index())
sub = pd.read_csv(os.path.join(MFG, "suburbs.csv"))
sidx = {s: i for i, s in enumerate(sub.suburb)}
o["si"] = o.suburb.map(sidx)
bysub = o.groupby(["m", "si"]).agg(sales=("amount_aud", "sum"), n=("order_id", "count"), uniq=("customer_id", "nunique")).round(2).reset_index()
cust = o.groupby("m").agg(uniq=("customer_id", "nunique"), new=("is_new_customer", "sum")).reset_index()
size = o.groupby(["m", "quantity"]).size().reset_index(name="n")
exp = pd.read_csv(os.path.join(MFG, "expenses.csv"))
kpi = pd.read_csv(os.path.join(MFG, "staff_kpi.csv"))
mfg = {
    "ord": rows(daily),      # date, line, promo, units, sales, promoCost, cogs, orders, newCustomers
    "exp": rows(exp),        # date, category, amount
    "suburbs": rows(sub[["suburb", "lat", "lon"]]),
    "bysub": rows(bysub),    # month, suburbIdx, sales, orders, uniqueCustomers
    "cust": rows(cust),      # month, uniqueCustomers, newCustomers
    "size": rows(size),      # month, unitsPerOrder, orders
    "staff": rows(kpi[["month", "staff", "total_made_aud", "kpi_target_aud", "base_salary_aud", "commission_aud", "bonus_aud"]]),
}

# ---------------- project 2: car rental overview ----------------
car = pd.read_csv(os.path.join(CAR, "car_info.csv"))
rev = pd.read_csv(os.path.join(CAR, "revenue_daily.csv"))
ev = pd.read_csv(os.path.join(CAR, "rental_events.csv"))
rev["m"] = pd.to_datetime(rev.date).dt.month
rdaily = rev.groupby("date").agg(amt=("amount_aud", "sum"), rented=("plate", "nunique")).reset_index()
rplate = rev.groupby(["m", "plate"]).amount_aud.sum().round(2).reset_index()
evd = ev.groupby(["date", "event"]).size().unstack(fill_value=0).reset_index()
for c in ("new_rent", "returned"):
    if c not in evd: evd[c] = 0
cexp = pd.read_csv(os.path.join(CAR, "expenses.csv"), **NA)
debt = pd.read_csv(os.path.join(CAR, "customer_debt.csv"))
carj = {
    "cars": rows(car[["plate", "make", "buying_price_aud", "status", "daily_rate_aud"]]),
    "rdaily": rows(rdaily),
    "rplate": rows(rplate),
    "events": rows(evd[["date", "new_rent", "returned"]]),
    "exp": rows(cexp[["date", "group", "category", "plate", "note", "amount_aud", "type"]]),
    "debt": rows(debt),
}

with open(os.path.join(OUT, "data.js"), "w", encoding="utf-8") as f:
    f.write("// SYNTHETIC sample data (seeded). Not real company data.\n")
    f.write("window.DATA = " + json.dumps({"mfg": mfg, "car": carj}, separators=(",", ":")) + ";\n")
print("data.js", os.path.getsize(os.path.join(OUT, "data.js")) // 1024, "KB")
