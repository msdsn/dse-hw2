# Income and Life Expectancy, 1952–2007

**Homework #2: Collaborative Data Wrangling & EDA**
**DSE 511 – Fall 2026**

**Team:** Partner A — *Mehmed* · Partner B — *Haneen*

Gapminder's country-year panel is one of the most widely used teaching datasets in
data science, but the raw export is not analysis-ready: it carries a meaningless
index column, terse camelCase names, and no derived measures. This repository
first turns that raw file into a documented, validated table
(`data/processed/gapminder_clean.csv`) and then uses it to study how a country's
income relates to how long its people live across 142 countries and 55 years.
Partner A owns the cleaning pipeline; Partner B owns the exploratory analysis.

---

## Dataset Information

| | |
|---|---|
| **Source** | Gapminder Foundation, distributed as the `gapminder` R package data extract (Bryan, J. 2017, *gapminder: Data from Gapminder*). Underlying data: <https://www.gapminder.org/data/> |
| **Date accessed** | 2 September 2026 |
| **File** | `data/raw/gapminder.csv` |
| **Size** | 100 KB · 1,704 rows × 6 variables (after dropping the exported row index) |
| **Scope** | 142 countries × 12 years (1952–2007, every 5th year) — a balanced panel |
| **License** | CC BY 4.0 (Gapminder) |

### Variables (raw)

| Column | Type | Unit / values | Description |
|---|---|---|---|
| `country` | text | 142 country names | Country, constant across years |
| `continent` | text | Africa, Americas, Asia, Europe, Oceania | Continent grouping |
| `year` | integer | 1952–2007, step 5 | Observation year |
| `lifeExp` | float | years | Life expectancy at birth |
| `pop` | integer | persons | Total population |
| `gdpPercap` | float | 2007 international \$ (PPP) | GDP per capita |

### Variables added during cleaning

| Column | Unit | Description |
|---|---|---|
| `gdp_total_bn` | billions of international \$ | `population × gdp_per_capita ÷ 1e9` |
| `log_gdp_per_capita` | log₁₀(international \$) | Log income — the scale on which the income/longevity relationship is linear |

### Data Cleaning (Partner A)

The pipeline is `src/clean_data.py`; run `python src/clean_data.py` from the
repository root. Each step prints what it checked and what it changed.

| Step | What it does | Result on this extract |
|---|---|---|
| 1. Drop export index | Removes the unnamed row-number column written by the R `write.csv` export | 7 columns → 6 |
| 2. Rename variables | `lifeExp` → `life_expectancy`, `pop` → `population`, `gdpPercap` → `gdp_per_capita` (snake_case throughout) | 6 descriptive names |
| 3. Enforce dtypes | `year` int16, `population` int64, `life_expectancy` and `gdp_per_capita` float64, `country` string (whitespace stripped), `continent` category | no silent type coercion downstream |
| 4. Missing values | Counts NA per column; drops any row missing a key variable | 0 missing, 0 rows dropped |
| 5. Integrity checks | Drops duplicate (`country`, `year`) keys; drops rows with non-positive life expectancy, GDP or population; confirms every country has all 12 years | 0 duplicates, 0 invalid, balanced panel |
| 6. Derived variables | `gdp_total_bn = population × gdp_per_capita / 1e9`; `log_gdp_per_capita = log10(gdp_per_capita)` | 6 columns → 8 |
| 7. Sort and write | Sorts by `country`, `year` and writes `data/processed/gapminder_clean.csv` | 1,704 rows × 8 columns, 142 countries, 1952–2007 |

The checks in steps 4 and 5 all pass with nothing removed, so the cleaned file has
the same 1,704 country-years as the raw one. They are kept in the pipeline so the
result is verified rather than assumed.

**Tools:** pandas 3.0 (reading, renaming, grouping, writing), numpy (log transform),
pathlib (paths relative to the repository root).

---
