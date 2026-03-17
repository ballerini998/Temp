import math
import pandas as pd
import numpy as np
import streamlit as st

try:
    import altair as alt
    HAS_ALTAIR = True
except Exception:
    HAS_ALTAIR = False

st.set_page_config(page_title="HEYE Dashboard", page_icon="🎓", layout="wide")

st.markdown(
    """
    <style>
    .main > div {padding-top: 1.2rem;}
    div[data-testid='stMetric'] {
        background: linear-gradient(135deg, rgba(34,139,230,0.10), rgba(111,66,193,0.10));
        border: 1px solid rgba(49, 51, 63, 0.12);
        border-radius: 16px;
        padding: 8px 10px;
    }
    h1, h2, h3 {letter-spacing: -0.02em;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Demo data
# -------------------------
territories = ["Bergamo", "Lombardia", "Italia"]
years = list(range(2019, 2025))

employment_df = pd.DataFrame({
    "year": years * 3,
    "territory": sum([[t] * len(years) for t in territories], []),
    "employment_rate": [61, 62, 63, 65, 66, 67,
                        64, 65, 66, 68, 69, 70,
                        58, 59, 60, 62, 63, 64],
    "neet_rate": [17, 16, 15, 14, 13, 12,
                   16, 15, 14, 13, 12, 11,
                   22, 21, 20, 18, 17, 16],
    "temporary_rate": [21, 20, 19, 20, 21, 20,
                       23, 22, 21, 22, 22, 21,
                       25, 24, 23, 24, 24, 23],
})

mobility_df = pd.DataFrame({
    "territory": np.repeat(territories, 3),
    "status": ["Stay", "Move within area", "Leave area"] * 3,
    "share": [68, 18, 14, 65, 19, 16, 72, 15, 13],
})

education_df = pd.DataFrame({
    "territory": np.repeat(territories, 3),
    "path": ["University", "ITS/technical", "Other"] * 3,
    "share": [45, 18, 37, 42, 20, 38, 35, 15, 50],
})

autonomy_df = pd.DataFrame({
    "territory": territories,
    "income_score": [67, 64, 55],
    "housing_score": [62, 58, 50],
    "job_score": [70, 66, 57],
    "autonomy_score": [66, 63, 54],
})

wellbeing_df = pd.DataFrame({
    "territory": territories,
    "perceived_stability": [6.8, 6.5, 5.9],
    "wellbeing": [7.0, 6.8, 6.3],
    "future_confidence": [6.6, 6.4, 5.8],
})

# -------------------------
# Helpers
# -------------------------
def section_header(title, text):
    st.markdown(f"## {title}")
    st.caption(text)


def altair_ready():
    return HAS_ALTAIR


def donut_chart(df, category_col, value_col, title=""):
    if not altair_ready():
        st.dataframe(df, use_container_width=True)
        return
    chart = (
        alt.Chart(df)
        .mark_arc(innerRadius=55, outerRadius=95)
        .encode(
            theta=alt.Theta(f"{value_col}:Q"),
            color=alt.Color(f"{category_col}:N", legend=alt.Legend(title="")),
            tooltip=[category_col, value_col],
        )
        .properties(height=260, title=title)
    )
    st.altair_chart(chart, use_container_width=True)


def bump_like_chart(df, value_col, title=""):
    if not altair_ready():
        st.line_chart(df.pivot(index="year", columns="territory", values=value_col))
        return
    chart = (
        alt.Chart(df)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y(f"{value_col}:Q", title=""),
            color=alt.Color("territory:N", legend=alt.Legend(title="")),
            tooltip=["territory", "year", value_col],
        )
        .properties(height=320, title=title)
    )
    st.altair_chart(chart, use_container_width=True)


def radar_like_heatmap(df, title=""):
    long_df = df.melt(id_vars="territory", var_name="dimension", value_name="score")
    if not altair_ready():
        st.dataframe(long_df, use_container_width=True)
        return
    chart = (
        alt.Chart(long_df)
        .mark_rect(cornerRadius=8)
        .encode(
            x=alt.X("dimension:N", title=""),
            y=alt.Y("territory:N", title=""),
            color=alt.Color("score:Q", scale=alt.Scale(scheme="blues"), title="Score"),
            tooltip=["territory", "dimension", "score"],
        )
        .properties(height=240, title=title)
    )
    text = alt.Chart(long_df).mark_text(baseline="middle").encode(
        x="dimension:N", y="territory:N", text=alt.Text("score:Q", format=".0f"),
        color=alt.condition(alt.datum.score > 62, alt.value("white"), alt.value("black"))
    )
    st.altair_chart(chart + text, use_container_width=True)


def lollipop_chart(df, value_col, title=""):
    if not altair_ready():
        st.bar_chart(df.set_index("territory")[value_col])
        return
    base = alt.Chart(df)
    rules = base.mark_rule(strokeWidth=3).encode(
        x=alt.X(f"{value_col}:Q", title=""),
        y=alt.Y("territory:N", sort="-x", title=""),
        x2=alt.value(0),
    )
    points = base.mark_circle(size=180).encode(
        x=f"{value_col}:Q",
        y=alt.Y("territory:N", sort="-x"),
        tooltip=["territory", value_col],
    )
    st.altair_chart((rules + points).properties(height=220, title=title), use_container_width=True)


# -------------------------
# Sidebar
# -------------------------
st.sidebar.title("HEYE Dashboard")
page = st.sidebar.radio(
    "Section",
    [
        "Overview",
        "Population & Education",
        "Employment & Job Quality",
        "Mobility & Retention",
        "Economic Autonomy",
        "Well-being & Perceptions",
        "Data Notes",
    ],
)

st.title("HEYE — Becoming Adults in an Uncertain Place")
st.caption("Prototype dashboard for Bergamo, Lombardia, and Italy. Values are placeholders for layout and storytelling.")

# -------------------------
# Pages
# -------------------------
if page == "Overview":
    latest = employment_df[employment_df["year"] == employment_df["year"].max()].set_index("territory")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Employment rate", f"{latest.loc['Bergamo', 'employment_rate']}%", "+1.0")
    c2.metric("NEET rate", f"{latest.loc['Bergamo', 'neet_rate']}%", "-1.0")
    c3.metric("Temporary work", f"{latest.loc['Bergamo', 'temporary_rate']}%", "-1.0")
    c4.metric("Autonomy score", f"{autonomy_df.set_index('territory').loc['Bergamo', 'autonomy_score']}", "+3")

    col1, col2 = st.columns([1.2, 1])
    with col1:
        bump_like_chart(employment_df, "employment_rate", "Employment trend")
    with col2:
        donut_chart(mobility_df[mobility_df["territory"] == "Bergamo"], "status", "share", "Bergamo mobility profile")

    st.markdown("### Main takeaways")
    st.write(
        "Bergamo stands above the national average on employment and autonomy, but the retention question remains central: the dashboard should show not only outcomes, but also who stays, who moves, and under what conditions."
    )

elif page == "Population & Education":
    section_header("Population & Education", "Educational pipeline and composition of youth pathways.")
    col1, col2 = st.columns([1.1, 1])
    with col1:
        donut_chart(education_df[education_df["territory"] == "Bergamo"], "path", "share", "Bergamo educational mix")
    with col2:
        lollipop_chart(education_df[education_df["path"] == "University"].rename(columns={"share": "university_share"}), "university_share", "University pathway share")

    st.dataframe(education_df, use_container_width=True)

elif page == "Employment & Job Quality":
    section_header("Employment & Job Quality", "Track labour market insertion, NEET, and precarity.")
    tab1, tab2, tab3 = st.tabs(["Employment", "NEET", "Temporary work"])
    with tab1:
        bump_like_chart(employment_df, "employment_rate", "Employment rates over time")
    with tab2:
        bump_like_chart(employment_df, "neet_rate", "NEET rates over time")
    with tab3:
        bump_like_chart(employment_df, "temporary_rate", "Temporary work over time")

elif page == "Mobility & Retention":
    section_header("Mobility & Retention", "Separate stay, internal moves, and exits from the area.")
    c1, c2 = st.columns([1, 1])
    with c1:
        donut_chart(mobility_df[mobility_df["territory"] == "Bergamo"], "status", "share", "Bergamo")
    with c2:
        donut_chart(mobility_df[mobility_df["territory"] == "Lombardia"], "status", "share", "Lombardia")
    st.dataframe(mobility_df, use_container_width=True)

elif page == "Economic Autonomy":
    section_header("Economic Autonomy", "Objective dimensions of youth autonomy and material stability.")
    radar_like_heatmap(autonomy_df, "Autonomy profile by territory")

elif page == "Well-being & Perceptions":
    section_header("Well-being & Perceptions", "Perceived stability, well-being, and future confidence.")
    st.dataframe(wellbeing_df, use_container_width=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Bergamo: perceived stability", wellbeing_df.set_index("territory").loc["Bergamo", "perceived_stability"])
    c2.metric("Bergamo: well-being", wellbeing_df.set_index("territory").loc["Bergamo", "wellbeing"])
    c3.metric("Bergamo: future confidence", wellbeing_df.set_index("territory").loc["Bergamo", "future_confidence"])

elif page == "Data Notes":
    section_header("Data Notes", "Prototype notes for the office version.")
    st.markdown(
        """
        - Replace demo values with public indicators for Bergamo, Lombardia, and Italy.
        - Use one CSV per theme or a single long-format file with territory, year, indicator, and value.
        - Keep a note for each chart: source, territorial level, update frequency, and whether the value is observed or provisional.
        - If you later install Plotly, Streamlit supports fully interactive Plotly charts directly.
        """
    )
