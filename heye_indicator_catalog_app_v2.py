import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="HEYE Dashboard Blueprint", layout="wide")

st.title("HEYE Dashboard Blueprint")
st.caption("Prototype of the dashboard structure, indicators, sources, and expected visual layout")

rows = [
    # Context
    {
        "Section": "Context and demography",
        "Indicator": "Age structure of the population",
        "Description": "Population by age groups; demographic context for Bergamo, Lombardia, and Italy.",
        "Source": "ISTAT Demo / PPC",
        "Provincial level already available?": "Yes",
        "Planned chart": "Population pyramid / grouped bars",
    },
    {
        "Section": "Context and demography",
        "Indicator": "Net migration by age",
        "Description": "Migration balance by age. International flows can be built at province level; internal flows are more solid at regional level.",
        "Source": "ISTAT Demo + ISTAT Esplora Dati (migrations)",
        "Provincial level already available?": "Partly",
        "Planned chart": "Age profile line / bars",
    },
    {
        "Section": "Context and demography",
        "Indicator": "Old-age dependency ratio (OADR)",
        "Description": "Population aged 65+ relative to population aged 15–64.",
        "Source": "ISTAT Demo / PPC",
        "Provincial level already available?": "Yes",
        "Planned chart": "Trend line",
    },
    {
        "Section": "Context and demography",
        "Indicator": "Ageing index",
        "Description": "Population aged 65+ relative to population aged 0–14.",
        "Source": "ISTAT Demo / PPC",
        "Provincial level already available?": "Yes",
        "Planned chart": "Trend line",
    },
    {
        "Section": "Context and demography",
        "Indicator": "Mean age",
        "Description": "Average age of the resident population.",
        "Source": "ISTAT Demo / PPC",
        "Provincial level already available?": "Yes",
        "Planned chart": "Dot plot / trend line",
    },
    {
        "Section": "Context and demography",
        "Indicator": "Share aged 80+",
        "Description": "Weight of the oldest-old population in the territory.",
        "Source": "ISTAT Demo / PPC",
        "Provincial level already available?": "Yes",
        "Planned chart": "Trend line",
    },
    # Core youth
    {
        "Section": "Core youth indicators",
        "Indicator": "Tertiary attainment (%)",
        "Description": "Share of people aged 25–34 with tertiary education; separated by sex where available.",
        "Source": "Eurostat; ISTAT/USTAT used to enrich local tertiary education block",
        "Provincial level already available?": "No (standard regional comparison)",
        "Planned chart": "Grouped bars by territory and sex",
    },
    {
        "Section": "Core youth indicators",
        "Indicator": "Tertiary attainment (absolute number)",
        "Description": "Number of people aged 25–34 with tertiary education; derived from attainment rate and population counts.",
        "Source": "Eurostat + population data",
        "Provincial level already available?": "No (standard regional comparison)",
        "Planned chart": "Bars / line trend",
    },
    {
        "Section": "Core youth indicators",
        "Indicator": "University enrolments",
        "Description": "Students enrolled in university; can be shown by institution and, where available, by sex.",
        "Source": "USTAT MUR",
        "Provincial level already available?": "No, but university level available",
        "Planned chart": "Bars by institution / trend line",
    },
    {
        "Section": "Core youth indicators",
        "Indicator": "University first-year entrants",
        "Description": "New entrants to university, useful to track local educational pipeline.",
        "Source": "USTAT MUR",
        "Provincial level already available?": "No, but university level available",
        "Planned chart": "Bars / trend line",
    },
    {
        "Section": "Core youth indicators",
        "Indicator": "University graduates",
        "Description": "Number of graduates; can support local tertiary education profile.",
        "Source": "USTAT MUR",
        "Provincial level already available?": "No, but university level available",
        "Planned chart": "Bars / trend line",
    },
    {
        "Section": "Core youth indicators",
        "Indicator": "ITS enrolments / diplomas",
        "Description": "Students enrolled in ITS Academy and diploma outcomes, where territorial detail is available.",
        "Source": "INDIRE ITS Academy monitoring",
        "Provincial level already available?": "To verify",
        "Planned chart": "Bars / KPI cards",
    },
    {
        "Section": "Core youth indicators",
        "Indicator": "Youth employment rate",
        "Description": "Employment rate of young people; can be separated by sex and sometimes by education.",
        "Source": "ISTAT Esplora Dati + Eurostat",
        "Provincial level already available?": "Often yes in ISTAT sources, to confirm by exact series",
        "Planned chart": "Grouped bars / trend line",
    },
    {
        "Section": "Core youth indicators",
        "Indicator": "Employment rate of young non-students by education and years since completion",
        "Description": "Employment of young people no longer in education, by attainment level and years since completion.",
        "Source": "Eurostat; Labour Force Survey may offer additional Italian detail",
        "Provincial level already available?": "No / unclear",
        "Planned chart": "Multi-line chart",
    },
    {
        "Section": "Core youth indicators",
        "Indicator": "NEET rate",
        "Description": "Young people not in employment, education or training; separated by sex where available.",
        "Source": "Eurostat",
        "Provincial level already available?": "No (regional comparison)",
        "Planned chart": "Grouped bars / trend line",
    },
    {
        "Section": "Core youth indicators",
        "Indicator": "Inactive youth",
        "Description": "Inactive young people outside the labour force; useful to complement employment and NEET.",
        "Source": "ISTAT Esplora Dati",
        "Provincial level already available?": "Yes",
        "Planned chart": "Bars / trend line",
    },
    {
        "Section": "Core youth indicators",
        "Indicator": "Youth mobility balance",
        "Description": "Youth inflow, outflow and balance. Internal migration can still matter even when moves stay within the broader community.",
        "Source": "ISTAT Esplora Dati + ISTAT Demo",
        "Provincial level already available?": "Partly (international yes; internal mainly regional)",
        "Planned chart": "Net balance bars + age profile",
    },
    {
        "Section": "Core youth indicators",
        "Indicator": "Housing burden / housing stress",
        "Description": "Proxy of economic pressure from housing costs.",
        "Source": "ISTAT BesT",
        "Provincial level already available?": "Yes",
        "Planned chart": "Bars / dot plot",
    },
    {
        "Section": "Core youth indicators",
        "Indicator": "Subjective well-being",
        "Description": "Indicator of life satisfaction or subjective well-being; can be split by sex where available.",
        "Source": "ISTAT BesT",
        "Provincial level already available?": "Yes",
        "Planned chart": "Bars / dot plot",
    },
    {
        "Section": "Core youth indicators",
        "Indicator": "Entry cohorts index (19, 21, 25)",
        "Description": "Number and index of cohorts reaching ages 19, 21, and 25 under demographic projections.",
        "Source": "ISTAT Demo / PPC",
        "Provincial level already available?": "Yes",
        "Planned chart": "Indexed trend lines",
    },
]

df = pd.DataFrame(rows)

with st.sidebar:
    st.header("Filters")
    section = st.multiselect("Section", options=df["Section"].unique(), default=list(df["Section"].unique()))
    prov = st.multiselect(
        "Provincial availability",
        options=df["Provincial level already available?"].unique(),
        default=list(df["Provincial level already available?"].unique()),
    )
    st.markdown("---")
    st.markdown("**Reading rule**")
    st.write("'Partly' means the indicator is available provincially only for some components or only after reconstruction.")

fdf = df[df["Section"].isin(section) & df["Provincial level already available?"].isin(prov)]

st.subheader("Operational schema")
st.dataframe(fdf[["Section", "Indicator", "Description", "Source", "Provincial level already available?"]], use_container_width=True, hide_index=True)

csv = fdf.to_csv(index=False).encode("utf-8")
st.download_button("Download schema as CSV", csv, file_name="heye_dashboard_schema.csv", mime="text/csv")

# small preview data for placeholder charts
preview_map = {
    "Population pyramid / grouped bars": pd.DataFrame({"Group": ["0-14", "15-24", "25-34", "35-64", "65+"], "Bergamo": [11, 10, 12, 42, 25]}),
    "Age profile line / bars": pd.DataFrame({"Age": [15, 20, 25, 30, 35], "Balance": [-1, 3, 7, 2, -2]}),
    "Trend line": pd.DataFrame({"Year": [2020, 2025, 2030, 2035, 2040], "Value": [100, 104, 109, 113, 118]}),
    "Dot plot / trend line": pd.DataFrame({"Territory": ["Bergamo", "Lombardia", "Italia"], "Value": [45.2, 46.8, 47.9]}),
    "Grouped bars by territory and sex": pd.DataFrame({"Territory": ["Bergamo", "Bergamo", "Lombardia", "Lombardia", "Italia", "Italia"], "Sex": ["F", "M", "F", "M", "F", "M"], "Value": [38, 32, 41, 35, 39, 33]}),
    "Bars / line trend": pd.DataFrame({"Year": [2018, 2019, 2020, 2021, 2022], "Value": [80, 83, 78, 85, 88]}),
    "Bars by institution / trend line": pd.DataFrame({"Institution": ["UniBg", "Milano", "Brescia"], "Value": [17000, 61000, 15000]}),
    "Bars / KPI cards": pd.DataFrame({"Category": ["Enrolled", "Graduates"], "Value": [1200, 850]}),
    "Grouped bars / trend line": pd.DataFrame({"Territory": ["Bergamo", "Lombardia", "Italia"], "Value": [61, 64, 58]}),
    "Multi-line chart": pd.DataFrame({"Years": [1, 2, 3, 4], "Low edu": [52, 57, 60, 62], "Medium edu": [68, 72, 74, 76], "High edu": [79, 83, 85, 87]}),
    "Net balance bars + age profile": pd.DataFrame({"Component": ["Inflow", "Outflow", "Balance"], "Value": [1200, 980, 220]}),
    "Bars / dot plot": pd.DataFrame({"Territory": ["Bergamo", "Lombardia", "Italia"], "Value": [22, 19, 24]}),
    "Indexed trend lines": pd.DataFrame({"Year": [2024, 2026, 2028, 2030, 2032], "Age 19": [100, 98, 95, 92, 89], "Age 21": [100, 99, 97, 94, 91], "Age 25": [100, 101, 100, 98, 95]}),
}

st.subheader("Visual preview by section")
for sec in fdf["Section"].unique():
    st.markdown(f"## {sec}")
    sdf = fdf[fdf["Section"] == sec]
    for _, r in sdf.iterrows():
        with st.container(border=True):
            c1, c2 = st.columns([1.3, 1])
            with c1:
                st.markdown(f"### {r['Indicator']}")
                st.write(r["Description"])
                st.markdown(f"**Source:** {r['Source']}")
                st.markdown(f"**Provincial level already available?** {r['Provincial level already available?']}")
                st.markdown(f"**Planned chart:** {r['Planned chart']}")
            with c2:
                pdata = preview_map.get(r["Planned chart"])
                if pdata is None:
                    st.info("Preview not available")
                else:
                    chart_type = r["Planned chart"]
                    if chart_type == "Population pyramid / grouped bars":
                        long = pdata.melt(id_vars="Group", var_name="Territory", value_name="Value")
                        chart = alt.Chart(long).mark_bar().encode(x="Group:N", y="Value:Q", color="Territory:N")
                    elif chart_type == "Age profile line / bars":
                        chart = alt.Chart(pdata).mark_line(point=True).encode(x="Age:Q", y="Balance:Q")
                    elif chart_type in ["Trend line", "Bars / line trend", "Indexed trend lines"]:
                        if chart_type == "Indexed trend lines":
                            long = pdata.melt(id_vars="Year", var_name="Series", value_name="Value")
                            chart = alt.Chart(long).mark_line(point=True).encode(x="Year:Q", y="Value:Q", color="Series:N")
                        else:
                            chart = alt.Chart(pdata).mark_line(point=True).encode(x=list(pdata.columns)[0]+":Q", y="Value:Q")
                    elif chart_type in ["Dot plot / trend line", "Bars / dot plot", "Grouped bars / trend line"]:
                        chart = alt.Chart(pdata).mark_bar().encode(x="Territory:N", y="Value:Q")
                    elif chart_type == "Grouped bars by territory and sex":
                        chart = alt.Chart(pdata).mark_bar().encode(x="Territory:N", y="Value:Q", color="Sex:N", xOffset="Sex:N")
                    elif chart_type == "Bars by institution / trend line":
                        chart = alt.Chart(pdata).mark_bar().encode(x="Institution:N", y="Value:Q")
                    elif chart_type == "Bars / KPI cards":
                        chart = alt.Chart(pdata).mark_bar().encode(x="Category:N", y="Value:Q")
                    elif chart_type == "Multi-line chart":
                        long = pdata.melt(id_vars="Years", var_name="Education", value_name="Value")
                        chart = alt.Chart(long).mark_line(point=True).encode(x="Years:Q", y="Value:Q", color="Education:N")
                    elif chart_type == "Net balance bars + age profile":
                        chart = alt.Chart(pdata).mark_bar().encode(x="Component:N", y="Value:Q")
                    else:
                        chart = alt.Chart(pdata).mark_bar().encode(x=list(pdata.columns)[0]+":N", y="Value:Q")
                    st.altair_chart(chart.properties(height=220), use_container_width=True)

st.markdown("---")
st.caption("This app is a layout prototype. Final charts will use downloaded data from Eurostat, ISTAT Demo, ISTAT Esplora Dati / BesT, USTAT MUR, and where useful INDIRE.")
