"""
clean_data.py -- Partner A
DSE 511, Homework #2: Collaborative Data Wrangling & EDA

Reads the raw Gapminder extract, applies a documented cleaning pipeline, and
writes a tidy analysis-ready file to data/processed/gapminder_clean.csv.

Run from the repository root:
    python src/clean_data.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "gapminder.csv"
PROCESSED = ROOT / "data" / "processed" / "gapminder_clean.csv"

# Step 2: descriptive snake_case names for every variable we keep.
RENAME = {
    "country": "country",
    "continent": "continent",
    "year": "year",
    "lifeExp": "life_expectancy",
    "pop": "population",
    "gdpPercap": "gdp_per_capita",
}

KEY_VARS = ["life_expectancy", "gdp_per_capita", "population"]


def load_raw() -> pd.DataFrame:
    """Step 1: read the raw file and drop the unnamed row-number column.

    The file was exported from R, so its first column is an unlabelled index
    ("", "1", "2", ...) that carries no information.
    """
    df = pd.read_csv(RAW)
    unnamed = [c for c in df.columns if c.startswith("Unnamed") or c == ""]
    df = df.drop(columns=unnamed)
    print(f"[1] loaded {RAW.name}: {df.shape[0]} rows x {df.shape[1]} cols "
          f"(dropped index columns: {unnamed})")
    return df


def rename_and_type(df: pd.DataFrame) -> pd.DataFrame:
    """Steps 2-3: rename variables and enforce explicit dtypes."""
    df = df.rename(columns=RENAME)[list(RENAME.values())]
    df["year"] = df["year"].astype("int16")
    df["population"] = df["population"].astype("int64")
    df["life_expectancy"] = df["life_expectancy"].astype("float64")
    df["gdp_per_capita"] = df["gdp_per_capita"].astype("float64")
    df["country"] = df["country"].str.strip().astype("string")
    df["continent"] = df["continent"].str.strip().astype("category")
    print(f"[2] renamed to snake_case: {list(df.columns)}")
    print(f"[3] dtypes enforced:\n{df.dtypes.to_string()}")
    return df


def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Step 4: report missing values and drop rows missing any key variable.

    This extract turns out to be complete, so nothing is dropped -- but the
    check is part of the pipeline so that the result is verified, not assumed.
    """
    na_counts = df.isna().sum()
    print("[4] missing values per column:")
    print(na_counts.to_string())
    before = len(df)
    df = df.dropna(subset=KEY_VARS)
    print(f"    dropped {before - len(df)} row(s) missing a key variable")
    return df


def validate(df: pd.DataFrame) -> pd.DataFrame:
    """Step 5: integrity checks -- duplicate keys, impossible values, panel shape."""
    dupes = df.duplicated(subset=["country", "year"]).sum()
    print(f"[5] duplicate (country, year) keys: {dupes}")
    df = df.drop_duplicates(subset=["country", "year"])

    bad = df[(df["life_expectancy"] <= 0)
             | (df["gdp_per_capita"] <= 0)
             | (df["population"] <= 0)]
    print(f"    rows with non-positive life_expectancy / gdp / population: {len(bad)}")
    df = df.drop(index=bad.index)

    per_country = df.groupby("country", observed=True)["year"].nunique()
    unbalanced = per_country[per_country != per_country.max()]
    print(f"    countries without the full {per_country.max()}-year panel: "
          f"{len(unbalanced)} {list(unbalanced.index)}")
    return df


def add_derived(df: pd.DataFrame) -> pd.DataFrame:
    """Step 6: derived variables used by the EDA.

    gdp_total_bn   -- total GDP in billions of 2007 international dollars.
    log_gdp_per_capita -- GDP per capita is right-skewed across three orders of
                          magnitude, so its log is the sensible scale for both
                          correlation and the scatterplot.
    """
    df = df.copy()
    df["gdp_total_bn"] = (df["population"] * df["gdp_per_capita"]) / 1e9
    df["log_gdp_per_capita"] = np.log10(df["gdp_per_capita"])
    print(f"[6] added derived columns: gdp_total_bn, log_gdp_per_capita")
    return df


def main() -> None:
    df = load_raw()
    df = rename_and_type(df)
    df = handle_missing(df)
    df = validate(df)
    df = add_derived(df)

    # Step 7: sort into a stable panel order and write the cleaned file.
    df = df.sort_values(["country", "year"]).reset_index(drop=True)
    PROCESSED.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED, index=False)
    print(f"[7] wrote {PROCESSED.relative_to(ROOT)}: "
          f"{df.shape[0]} rows x {df.shape[1]} cols, "
          f"{df['country'].nunique()} countries, "
          f"{df['year'].min()}-{df['year'].max()}")


if __name__ == "__main__":
    main()
