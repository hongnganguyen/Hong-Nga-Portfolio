"""Aggregate the SYNTHETIC CSVs into docs/data.js for the interactive dashboard.
Run after tools/generate.py:  python tools/build_dashboard.py"""
import os, json
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RET = os.path.join(ROOT, "projects", "automotive-glass-service-powerbi", "data")
CAR = os.path.join(ROOT, "projects", "car-rental-overview-powerbi", "data")
OUT = os.path.join(ROOT, "docs")
os.makedirs(OUT, exist_ok=True)


def rows(df):
    return json.loads(df.to_json(orient="values"))


# ---- automotive glass service ----
rev = pd.read_csv(os.path.join(RET, "daily_revenue.csv"), parse_dates=["date"], keep_default_na=False)  # "None" = no promotion, not missing
rev["m"] = rev.date.dt.month
orders = (rev.groupby(["m", "branch_id", "vehicle_segment", "promotion_name"])
          .agg(sales=("amount_vnd", "sum"), promo=("promo_expense_vnd", "sum"), cogs=("cogs_vnd", "sum"), n=("order_id", "count"))
          .reset_index())
exp = pd.read_csv(os.path.join(RET, "expenses.csv"))
kpi = pd.read_csv(os.path.join(RET, "staff_kpi.csv"))
br = pd.read_csv(os.path.join(RET, "branches.csv"))
retail = {
    "branches": br[["branch_id", "branch_name"]].values.tolist(),
    "orders": rows(orders),            # m, branch, segment, promo, sales, promo_exp, cogs, n
    "exp": rows(exp[["month", "branch_id", "category", "amount_vnd"]]),
    "kpi": rows(kpi[["month", "staff", "total_made_vnd", "kpi_target_vnd", "bonus_vnd", "base_salary_vnd"]]),
}

# ---- car rental ----
car = pd.read_csv(os.path.join(CAR, "car_info.csv"))
rw = pd.read_csv(os.path.join(CAR, "revenue_weekly.csv"), parse_dates=["week_start"])
rw["m"] = rw.week_start.dt.month
rw = rw.groupby(["m", "plate"]).agg(amt=("amount_aud", "sum"), new=("new_rent", "sum"), ret=("returned", "sum")).reset_index()
mat = pd.read_csv(os.path.join(CAR, "expenses_material.csv"))
hr = pd.read_csv(os.path.join(CAR, "expenses_hr.csv")).groupby("month").total_aud.sum().reset_index()
off = pd.read_csv(os.path.join(CAR, "expenses_office.csv"))
debt = pd.read_csv(os.path.join(CAR, "customer_debt.csv"))
carj = {
    "cars": car[["plate", "make", "buying_price_aud", "status"]].values.tolist(),
    "rev": rows(rw),                   # m, plate, amt, new, ret
    "mat": rows(mat[["month", "plate", "category", "expense_aud", "type"]]),
    "hr": rows(hr),
    "off": rows(off),
    "debt": rows(debt[["customer_id", "plate", "outstanding_aud"]]),
}

with open(os.path.join(OUT, "data.js"), "w", encoding="utf-8") as f:
    f.write("// SYNTHETIC sample data (seeded). Not real company data.\n")
    f.write("window.DATA = " + json.dumps({"retail": retail, "car": carj}, separators=(",", ":")) + ";\n")
print("data.js", os.path.getsize(os.path.join(OUT, "data.js")) // 1024, "KB")
