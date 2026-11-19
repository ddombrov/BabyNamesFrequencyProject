from pathlib import Path

import pandas as pd
import streamlit as st
from census import lookup_census_first_name

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_DIRS = [ROOT / "main" / "Testing Files", ROOT / "names3to4" / "Testing Files"]
COLUMNS = ["Year", "Sex", "Rank", "Name", "Count"]
HEADER_ALIASES = {
    "Sex": {"Sex", "Sexes", "Gender", "Genders"},
    "Name": {"Name", "Names", "First Name"},
    "Count": {"Count", "Counts", "Frequency", "Frequencies", "Value", "Values",
              "Total", "Totals", "Number", "Numbers"},
    "Rank": {"Rank", "Ranks", "Position", "Positions"},
    "Year": {"Year", "Years"},
}
ETHNICITY_COLUMNS = {
    "pctwhite": "% White",
    "pctblack": "% Black",
    "pctapi": "% Asian / Pacific Islander",
    "pctaian": "% American Indian / Alaska Native",
    "pct2prace": "% Two or more races",
    "pcthispanic": "% Hispanic",
}


def normalize(df):
    renames = {}
    for header in df.columns:
        title = str(header).strip().title()
        for target, aliases in HEADER_ALIASES.items():
            if title in aliases:
                renames[header] = target
    df = df.rename(columns=renames)
    df = df[[c for c in COLUMNS if c in df.columns]].copy()
    if "Name" in df.columns:
        df["Name"] = df["Name"].astype(str).str.strip().str.upper()
    for col in ("Year", "Rank", "Count"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def read_table(source, filename):
    if filename.lower().endswith((".xlsx", ".xlsm")):
        return pd.read_excel(source)
    return pd.read_csv(source, encoding="latin1")


@st.cache_data
def load_example(path):
    return normalize(read_table(path, path))


@st.cache_data
def ethnicity_for(names):
    result = lookup_census_first_name(pd.DataFrame({"Name": names}), "Name")
    result = result[["Name", *ETHNICITY_COLUMNS, "race"]].dropna(subset=["pctwhite"])
    return result.rename(columns={**ETHNICITY_COLUMNS, "race": "Most likely"})


def examples():
    files = {}
    for folder in EXAMPLE_DIRS:
        for path in sorted(folder.rglob("*.csv")):
            files[str(path.relative_to(ROOT))] = str(path)
    return files


ICONS = Path(__file__).resolve().parent / "icons"
st.set_page_config(page_title="Baby Name Data", page_icon=str(ICONS / "chart-up.png"), layout="wide")
icon_column, title_column = st.columns([1, 14], vertical_alignment="center")
icon_column.image(str(ICONS / "chart-line.png"), width=72)
title_column.title("Baby Name Data")

with st.sidebar:
    st.image(str(ICONS / "chart-down.png"), width=64)
    st.header("Data file")
    mode = st.radio("Source", ["Pick an example", "Upload my own"])
    if mode == "Pick an example":
        options = examples()
        choice = st.selectbox("Example file", list(options))
        df, label = load_example(options[choice]), choice
    else:
        upload = st.file_uploader("CSV or Excel file", type=["csv", "xlsx", "xlsm"])
        if upload is None:
            st.info("Upload a file to get started.")
            st.stop()
        df, label = normalize(read_table(upload, upload.name)), upload.name

if df.empty or "Name" not in df.columns:
    st.error(f"{label} has no name data in a recognised format.")
    st.stop()

has_years = "Year" in df.columns and df["Year"].notna().any()
has_counts = "Count" in df.columns and df["Count"].notna().any()

tabs = st.tabs(["Ethnicity", "Search", "Top 10", "Graph", "Alphabetical", "Data"])

with tabs[0]:
    names = tuple(sorted(df["Name"].dropna().unique()))
    result = ethnicity_for(names)
    st.write(f"Matched {len(result):,} of {len(names):,} distinct names.")
    st.dataframe(result, hide_index=True, width="stretch",
                 column_config={c: st.column_config.NumberColumn(format="%.2f")
                                for c in ETHNICITY_COLUMNS.values()})
    if not result.empty:
        st.bar_chart(result["Most likely"].value_counts())

with tabs[1]:
    term = st.text_input("Search names containing")
    if term:
        matches = df[df["Name"].str.contains(term, case=False, regex=False)]
        st.write(f"{len(matches):,} matching rows")
        st.dataframe(matches, hide_index=True, width="stretch")

with tabs[2]:
    subset = df
    cols = st.columns(2)
    if has_years:
        years = sorted(df["Year"].dropna().astype(int).unique(), reverse=True)
        year = cols[0].selectbox("Year", years)
        subset = subset[subset["Year"] == year]
    if "Sex" in df.columns:
        sex = cols[1].selectbox("Sex", ["All", *sorted(df["Sex"].dropna().astype(str).unique())])
        if sex != "All":
            subset = subset[subset["Sex"].astype(str) == sex]
    if has_counts:
        top = subset.groupby("Name")["Count"].sum().sort_values(ascending=False).head(10)
        st.dataframe(top.reset_index(), hide_index=True)
        st.bar_chart(top)
    elif "Rank" in subset.columns:
        st.dataframe(subset.sort_values("Rank").head(10), hide_index=True)
    else:
        st.warning("This file has no Count or Rank column to rank names by.")

with tabs[3]:
    if not (has_years and has_counts and df["Year"].nunique() > 1):
        st.warning("Graphs need a file with counts across more than one year.")
    else:
        all_names = sorted(df["Name"].dropna().unique())
        default = [n for n in ("OLIVER", "JAMES") if n in all_names] or all_names[:1]
        picked = st.multiselect("Names to compare", all_names, default=default)
        if picked:
            trend = (df[df["Name"].isin(picked)]
                     .groupby(["Year", "Name"])["Count"].sum()
                     .unstack("Name"))
            trend.index = trend.index.astype(int).astype(str)
            st.line_chart(trend, x_label="Year", y_label="Frequency")

with tabs[4]:
    st.dataframe(df.sort_values("Name"), hide_index=True, width="stretch")

with tabs[5]:
    st.dataframe(df, hide_index=True, width="stretch")
    st.download_button("Download as CSV", df.to_csv(index=False), file_name="names.csv")
