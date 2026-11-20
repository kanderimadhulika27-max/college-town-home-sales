# College-Town Home Sales

## What this site is for

A dashboard of 35,442 home sales near 11 university campuses (18 cities, 11 states, March 2023 to March 2026). It answers: what do homes sell for in each college town, how have prices changed by quarter, and how fast do homes go under contract? It is for anyone comparing college towns, especially students and families looking at Champaign-Urbana.

## Live site

https://kanderimadhulika27-max.github.io/college-town-home-sales/

## Data notes

- All numbers are computed from `data/college_town_home_sales.csv` by `scripts/build_summary.py`, which writes `data/summary.json` for the page. The dataset files are not modified.
- **Prices:** sales under $10,000 are left out (40 sales). Medians are used instead of averages, so the 31 sales over $5,000,000 don't distort the results.
- **Days on market:** `contract_date` minus `list_date`, only for the 28,042 sales with both dates. A blank date is never treated as zero. The city table shows the share of sales with no list date.
- **Price per sq ft:** leaves out homes whose living area is 0 or missing.
- **Repeated addresses:** rows are never removed by address, since many are separate condo units. `listing_id` is the key.
- **`home_type`:** not used, because it is unreliable.
- **Quarterly chart:** whole quarters only (2023 Q2 to 2026 Q1), grouped by nearest campus.

## Tools we used

- Claude (AI coding agent) for the summary script, the page and debugging the publish. See `AGENT_LOG.md`.
- Plain HTML, CSS and JavaScript, with hand-drawn SVG charts.
- Python with pandas for `scripts/build_summary.py`.
- GitHub Pages and GitHub Actions for hosting.

## Citation

College-town home sales dataset, version 1.0 (2026). University of Illinois-Deloitte Foundation Center for Business Emerging Technologies. Data collected March 2026.
