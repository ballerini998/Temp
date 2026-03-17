import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="HEYE Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Helpers
# -----------------------------
@st.cache_data

def load_demo_data():
    years = list(range(2015, 2026))
    territories = ["Bergamo", "Lombardia", "Italia"]

    rows = []
    for year in years:
        for territory in territories:
            base = {
                "Bergamo": 1.00,
                "Lombardia": 1.08,
                "Italia": 0.97,
            }[territory]
            rows.append(
                {
                    "year": year,
                    "territory": territory,
                    "neet_rate": round((14 - 0.18 * (year - 2015)) * (1.05 if territory == "Italia" else 1.0) / base, 1),
                    "employment_rate": round((52 + 0.35 * (year - 2015)) * base, 1),
                    "temporary_rate": round((15 - 0.08 * (year - 2015)) * (1.02 if territory == "Italia" else 1.0), 1),
                    "part_time_invol": round((9 - 0.10 * (year - 2015)) * (1.1 if territory == "Italia" else 1.0) / base, 1),
                    "inflow_young": int((4200 + 60 * (year - 2015)) * base),
                    "outflow_young": int((3900 + 35 * (year - 2015)) * (1.03 if territory == "Bergamo" else 1.0)),
                    "higher_ed_share": round((23 + 0.55 * (year - 2015)) * base, 1),
                    "youth_population": int((180000 - 1200 * (year - 2015)) * base),
                    "income_eq_index": round((100 + 1.1 * (year - 2015)) * base, 1),
                    "housing_burden": round((25 - 0.20 * (year - 2015)) * (1.1 if territory == "Italia" else 1.0) / base, 1),
                    "life_satisfaction": round((6.8 + 0.03 * (year - 2015)) * (1.02 if territory == "Bergamo" else 1.0), 2),
                    "future_confidence": round((5.9 + 0.04 * (year - 2015)) * (1.02 if territory == "Lombardia" else 1.0), 2),
                }
            )
    df = pd.DataFrame(rows)
    df["net_migration_young"] = df["inflow_young"] - df["outflow_young"]
    return df


def kpi_card(label, value, help_text=None):
    st.metric(label=label, value=value, help=help_text)


def line_chart(df, y, title, y_label=None):
    fig = px.line(
        df,
        x="year",
        y=y,
        color="territory",
        markers=True,
        title=title,
    )
    fig.update_layout(height=420, legend_title_text="")
    fig.update_yaxes(title=y_label or y)
    st.plotly_chart(fig, use_container_width=True)


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("HEYE")
st.sidebar.caption("Higher Education and Youth Employability")
page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Population & Education",
        "Employment & Job Quality",
        "Mobility & Retention",
        "Economic Autonomy",
        "Well-being & Perceptions",
        "Data Notes",
    ],
)

df = load_demo_data()
year_selected = st.sidebar.slider("Year", int(df["year"].min()), int(df["year"].max()), int(df["year"].max()))
territory_focus = st.sidebar.selectbox("Highlight territory", ["Bergamo", "Lombardia", "Italia"])

current = df[df["year"] == year_selected].copy()
focus_row = current[current["territory"] == territory_focus].iloc[0]

# -----------------------------
# Pages
# -----------------------------
if page == "Home":
    st.title("HEYE Dashboard")
    st.subheader("Becoming Adults in an Uncertain Place")
    st.write(
        "Prototype dashboard for Bergamo, Lombardia, and Italy. "
        "Numbers are placeholders and must be replaced with real data as soon as the data pipeline is ready."
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Youth population", f"{focus_row['youth_population']:,}")
    with c2:
        kpi_card("Higher education share", f"{focus_row['higher_ed_share']:.1f}%")
    with c3:
        kpi_card("Employment rate", f"{focus_row['employment_rate']:.1f}%")
    with c4:
        kpi_card("Net youth migration", f"{int(focus_row['net_migration_young']):,}")

    left, right = st.columns(2)
    with left:
        line_chart(df, "employment_rate", "Employment rate")
    with right:
        line_chart(df, "net_migration_young", "Net youth migration")

    st.info(
        "Use this home page for the opening slide: 4 headline numbers + 2 trend charts + a short takeaway."
    )

elif page == "Population & Education":
    st.title("Population & Education")
    c1, c2 = st.columns(2)
    with c1:
        line_chart(df, "youth_population", "Youth population (15–34)")
    with c2:
        line_chart(df, "higher_ed_share", "Share with tertiary education")

    latest = current[["territory", "youth_population", "higher_ed_share"]].sort_values("territory")
    st.dataframe(latest, use_container_width=True, hide_index=True)

elif page == "Employment & Job Quality":
    st.title("Employment & Job Quality")
    top1, top2, top3, top4 = st.columns(4)
    with top1:
        kpi_card("Employment", f"{focus_row['employment_rate']:.1f}%")
    with top2:
        kpi_card("NEET", f"{focus_row['neet_rate']:.1f}%")
    with top3:
        kpi_card("Temporary jobs", f"{focus_row['temporary_rate']:.1f}%")
    with top4:
        kpi_card("Involuntary PT", f"{focus_row['part_time_invol']:.1f}%")

    c1, c2 = st.columns(2)
    with c1:
        line_chart(df, "employment_rate", "Employment rate")
        line_chart(df, "temporary_rate", "Temporary employment")
    with c2:
        line_chart(df, "neet_rate", "NEET rate")
        line_chart(df, "part_time_invol", "Involuntary part-time")

elif page == "Mobility & Retention":
    st.title("Mobility & Retention")
    top1, top2, top3 = st.columns(3)
    with top1:
        kpi_card("Youth inflow", f"{int(focus_row['inflow_young']):,}")
    with top2:
        kpi_card("Youth outflow", f"{int(focus_row['outflow_young']):,}")
    with top3:
        kpi_card("Net migration", f"{int(focus_row['net_migration_young']):,}")

    c1, c2 = st.columns(2)
    with c1:
        line_chart(df, "inflow_young", "Youth inflow")
        line_chart(df, "net_migration_young", "Net youth migration")
    with c2:
        line_chart(df, "outflow_young", "Youth outflow")

    st.markdown(
        "**Suggested HEYE takeaway:** do not look only at saldo. Separate attraction and retention."
    )

elif page == "Economic Autonomy":
    st.title("Economic Autonomy")
    c1, c2 = st.columns(2)
    with c1:
        line_chart(df, "income_eq_index", "Equivalent income index")
    with c2:
        line_chart(df, "housing_burden", "Housing cost burden")

    st.caption(
        "This page can later host a composite indicator of youth stability/autonomy."
    )

elif page == "Well-being & Perceptions":
    st.title("Well-being & Perceptions")
    c1, c2 = st.columns(2)
    with c1:
        line_chart(df, "life_satisfaction", "Life satisfaction")
    with c2:
        line_chart(df, "future_confidence", "Confidence in the future")

    st.warning(
        "For this page, replace placeholders only with survey-based measures that really exist in the chosen data source."
    )

elif page == "Data Notes":
    st.title("Data Notes")
    st.markdown(
        """
        ### Suggested real-data structure
        Your tidy input file should have one row by `year x territory`.

        **Required columns for this prototype**
        - `year`
        - `territory` (`Bergamo`, `Lombardia`, `Italia`)
        - `youth_population`
        - `higher_ed_share`
        - `employment_rate`
        - `neet_rate`
        - `temporary_rate`
        - `part_time_invol`
        - `inflow_young`
        - `outflow_young`
        - `income_eq_index`
        - `housing_burden`
        - `life_satisfaction`
        - `future_confidence`

        ### Next step
        Replace `load_demo_data()` with a function that reads a CSV or parquet file.
        """
    )

