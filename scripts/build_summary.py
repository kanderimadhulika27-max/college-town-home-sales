"""Build data/summary.json, the numbers shown on index.html.

Reads data/college_town_home_sales.csv (never modified) and writes a small JSON
summary so the page loads fast. Run from the repository root:

    python3 scripts/build_summary.py

Rules applied (also stated on the page):
- Price figures use sales of $10,000 or more (40 sales under $10,000 are left out).
- Price per square foot also needs living_area_sqft > 0.
- Days on market = contract_date - list_date, only on rows with both dates.
  A blank date is never treated as zero.
- Quarterly trend uses whole quarters only: 2023 Q2 through 2026 Q1.
  (The data starts 2023-03-27, so 2023 Q1 has only a few days.)
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "college_town_home_sales.csv"
OUT = ROOT / "data" / "summary.json"

MIN_PRICE = 10_000

df = pd.read_csv(SRC, dtype={"zipcode": str, "county_fips": str, "parcel_number": str})
for c in ("list_date", "contract_date", "sale_date"):
    df[c] = pd.to_datetime(df[c])

df["dom"] = (df["contract_date"] - df["list_date"]).dt.days
priced = df[df["sale_price"] >= MIN_PRICE].copy()
sqft_ok = priced[priced["living_area_sqft"] > 0]
ppsf = sqft_ok["sale_price"] / sqft_ok["living_area_sqft"]


def r(x, nd=0):
    return None if pd.isna(x) else (int(round(x)) if nd == 0 else round(float(x), nd))


cities = []
for (city, state), g in df.groupby(["city", "state"]):
    gp = priced[(priced.city == city) & (priced.state == state)]
    gs = sqft_ok[(sqft_ok.city == city) & (sqft_ok.state == state)]
    dom = g["dom"].dropna()
    cities.append({
        "city": city,
        "state": state,
        "university": g["university"].mode().iloc[0],
        "sales": int(len(g)),
        "priced_sales": int(len(gp)),
        "median_price": r(gp["sale_price"].median()),
        "median_ppsf": r((gs["sale_price"] / gs["living_area_sqft"]).median()),
        "median_dom": r(dom.median()),
        "dom_n": int(len(dom)),
        "pct_no_list_date": r(g["list_date"].isna().mean() * 100, 1),
        "median_year_built": r(g["year_built"].median()),
        "median_sqft": r(g.loc[g.living_area_sqft > 0, "living_area_sqft"].median()),
    })
cities.sort(key=lambda c: -c["median_price"])

# Quarterly median price, overall and per campus area
q = priced.dropna(subset=["sale_date"]).copy()
q["quarter"] = q["sale_date"].dt.to_period("Q").astype(str)
quarters = [p for p in sorted(q["quarter"].unique()) if "2023Q2" <= p <= "2026Q1"]
q = q[q["quarter"].isin(quarters)]


def trend(frame):
    s = frame.groupby("quarter")["sale_price"].agg(["median", "size"])
    return [{"q": p, "median": r(s.loc[p, "median"]) if p in s.index else None,
             "n": int(s.loc[p, "size"]) if p in s.index else 0} for p in quarters]


trends = {"All campus areas": trend(q)}
for u, g in sorted(q.groupby("university")):
    trends[u] = trend(g)

summary = {
    "rule_min_price": MIN_PRICE,
    "total_sales": int(len(df)),
    "priced_sales": int(len(priced)),
    "excluded_under_min": int((df["sale_price"] < MIN_PRICE).sum()),
    "n_cities": int(df.groupby(["city", "state"]).ngroups),
    "n_states": int(df["state"].nunique()),
    "n_universities": int(df["university"].nunique()),
    "median_price": r(priced["sale_price"].median()),
    "median_ppsf": r(ppsf.median()),
    "median_dom": r(df["dom"].dropna().median()),
    "dom_n": int(df["dom"].notna().sum()),
    "first_sale": str(df["sale_date"].min().date()),
    "last_sale": str(df["sale_date"].max().date()),
    "cities": cities,
    "quarters": quarters,
    "trends": trends,
}
OUT.write_text(json.dumps(summary, indent=1))
print(f"Wrote {OUT.relative_to(ROOT)}: {len(cities)} cities, {len(quarters)} quarters")
