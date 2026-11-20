# Agent log

Add a dated entry each time you work with your AI coding agent, with the newest entry at the bottom. Each entry records what you asked the agent, what it produced, and what you checked or changed. Paste your key prompts in exactly as you typed them. Include at least one time the agent got something wrong, and how you caught it.

## 2026-11-19: Setup
- **Asked:** "Read AGENTS.md and docs/data_description_sheet.md and summarize the five data problems I need to handle."
- **Agent produced:** A summary of the five issues: blank dates, repeated addresses, impossible prices, unreliable home_type, and impossible sizes/taxes.
- **Checked or changed:** Read the sheet myself and decided on a rule: leave out sales under $10,000.

## 2026-11-19: First page
- **Asked:** "Replace the placeholder index.html with a table of median sale price per city from the CSV. Leave out sales under $10,000 and say so on the page."
- **Agent produced:** A table of 18 cities with median prices.
- **Checked or changed:** Compared 3 cities with the data sheet. One median showed $876,985.5, so I asked for whole dollars.

## 2026-11-19: Speed
- **Asked:** "The page is slow because it loads the full CSV. Write a script in scripts/ that saves a small summary JSON, and load that instead."
- **Agent produced:** A Python script and a summary JSON file.
- **Checked or changed:** Re-ran the script and confirmed the numbers didn't change.

## 2026-11-19: Charts
- **Asked:** "Add a bar chart of median price by city and a line chart of median price by quarter."
- **Agent produced:** Both charts.
- **Checked or changed:** The line chart included a quarter with only 5 days of sales, which made a fake dip. Asked it to use whole quarters only.

## 2026-11-19: Days on market
- **Asked:** "Add median days on market per city, using contract_date minus list_date only when both exist."
- **Agent produced:** A new table column.
- **Checked or changed:** The agent first used sale_date minus list_date. Caught it because the numbers were around 50 days instead of the sheet's 11, and asked for a fix.

## 2026-11-19: README and submit
- **Asked:** "Fill in the README sections: purpose, live link, data notes, tools used."
- **Agent produced:** A completed README.
- **Checked or changed:** Fixed the live link, checked the site in incognito, and submitted.
