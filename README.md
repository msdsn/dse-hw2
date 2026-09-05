# Income and Life Expectancy, 1952–2007

**Homework #2: Collaborative Data Wrangling & EDA**
**DSE 511 – Fall 2026**

**Team:** Partner A — *Mehmed* · Partner B — *Haneen*

This repository takes the Gapminder country-year panel, cleans it into an
analysis-ready table, and asks one question of it: **how are national income and
life expectancy related, and how has that relationship changed over fifty-five
years?** The short answer is that the two move together strongly — but on a *log*
income scale, and with Africa as a large and instructive exception.

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

---
