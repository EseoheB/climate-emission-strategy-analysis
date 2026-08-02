# Climate Emission Strategy Analysis

A data analysis project using the Climate TRACE Emission Reduction Solutions dataset to answer a
practical question: when a sector or country has several possible ways to cut emissions, which one
should actually come first, the option with the biggest raw impact, or the one that delivers strong
impact for the least effort? The analysis is also served as a queryable API, containerized with
Docker, so the ranking can be looked up on demand rather than only read as a static report.

## The Problem

Reduction potential is not spread evenly across industries, and within a given industry there is
often more than one way to cut emissions. Ranking those options by raw tonnage alone can be
misleading, since the biggest number on paper is not always the most realistic one to act on. This
project ranks strategies two ways, by total impact and by impact adjusted for implementation
difficulty, and identifies where those two rankings disagree.

## Dataset

Climate TRACE, `ers_plan_global_v5_9_0.csv` (July 2026 release). Source: https://climatetrace.org/data

- 2,406,480 rows, each pairing one emissions source with one applicable reduction strategy
- 63 sectors, 86 named strategies, 249 countries
- Each row includes a total reduction estimate (tonnes CO2e per year) and a difficulty score from 1
  (easiest) to 10 (hardest, or not yet well characterized)
- All emissions expressed in a single standardized unit (CO2e, 100 year timeframe), so totals across
  sectors and gases can be directly compared

Raw data is not included in this repo due to file size. Download it directly from the link above.

## Method

1. Load and validate the full dataset (row count, column types, missing values)
2. Aggregate by sector to find where reduction potential is concentrated
3. Aggregate by sector and strategy together, then add a priority score
   (`total_reduction / avg_difficulty`) alongside the raw impact ranking
4. Rank strategies within each sector both ways and isolate where the two rankings disagree
5. Visualize the tradeoff for the clearest example
6. Repeat the sector and strategy breakdown for a single country (Nigeria) to check scale
7. Serve the ranked results through a Flask API, containerized with Docker

## Key Findings

**Reduction potential is concentrated in a small number of sectors.** The top 15 of 63 sectors account
for 87.8% of total global reduction potential (26.3B of 29.9B tonnes CO2e per year). Electricity
generation alone, through solar replacement, represents roughly 8.9B tonnes per year.

**Most sectors have one dominant strategy.** In electricity generation, road transportation, and
forest management, one strategy is so far ahead of the alternatives that ranking it is trivial.

**A smaller group of sectors have real tradeoffs, and this is where the two ranking methods disagree.**
Five sectors showed a difference between ranking by raw impact and ranking by priority score:
domestic wastewater treatment, enteric fermentation (cattle operations), oil and gas refining, and
solid waste disposal, with solid waste disposal showing the largest shift.

In solid waste disposal, "Unspecified solution" ranks first by raw tonnage (47.2M t/yr) but carries a
difficulty score of nearly 10, meaning it is an uncharacterized catch-all rather than a defined plan.
Once difficulty is factored in, it drops to fifth. Three real landfill diversion and gas capture
strategies move ahead of it, led by "Diversion and biocover (sanitary landfill)" at 40.4M t/yr with a
difficulty score of 3.0, nearly the same benefit for a fraction of the effort.

**Country-level scale check (Nigeria).** Nigeria's total addressable reduction potential across all
sectors is 192M tonnes per year, 0.641% of the global total. Its top three levers are EV transition in
road transport, residue removal without burning in cropland fires, and carbon capture in cement
production.

## Running the API Locally

Build and run the containerized API:

```bash
docker build -t climate-strategy-api -f docker/Dockerfile .
docker run -p 5000:5000 climate-strategy-api
```

Then query it, for example:

http://127.0.0.1:5000/strategies?sector=cement


Returns ranked strategies for the given sector, sorted by priority score (impact adjusted for
implementation difficulty).

## Tools

Python, pandas, matplotlib, Google Colab, Flask, Docker

## Project Structure

notebooks/
climate_trace_analysis.ipynb
outputs/
sector_strategy_rankings.csv
docs/
findings.md
api/
app.py
docker/
Dockerfile
k8s/
terraform/


## Author

Rabiat Blessing Ibrahim
