"""The U.S. Census Bureau's 2020 first-name table (public domain), and a lookup that matches
ethnicolr's lookup_census_first_name, without its machine learning dependencies."""
from functools import lru_cache
from pathlib import Path

import pandas as pd

PERCENTAGE_COLUMNS = ["pctwhite", "pctblack", "pctapi", "pctaian", "pct2prace", "pcthispanic"]
CATEGORIES = ["white", "black", "api", "aian", "2prace", "hispanic"]
TABLE = Path(__file__).resolve().parent / "census_2020_first_names.csv.gz"


@lru_cache(maxsize=1)
def _table():
    return pd.read_csv(TABLE, keep_default_na=False, na_values=[""]).set_index("name")


def lookup_census_first_name(data, first_name_column):
    """Adds the six percentage columns and the most likely category ("race") for each first name.
    Names missing from the table get empty values."""
    keys = data[first_name_column].fillna("").astype(str).str.strip().str.upper()
    matched = _table().reindex(keys)
    result = data.copy()
    for column in PERCENTAGE_COLUMNS:
        result[column] = matched[column].to_numpy()
    percentages = result[PERCENTAGE_COLUMNS]
    found = percentages.notna().any(axis=1)
    result["race"] = None
    result.loc[found, "race"] = percentages[found].idxmax(axis=1).map(dict(zip(PERCENTAGE_COLUMNS, CATEGORIES)))
    return result
