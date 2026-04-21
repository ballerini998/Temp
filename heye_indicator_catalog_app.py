import pandas as pd
import streamlit as st

st.set_page_config(page_title='HEYE Indicator Catalog', page_icon='📊', layout='wide')

st.markdown(
    """
    <style>
    .main > div {padding-top: 1.1rem;}
    .indicator-card {
        border: 1px solid rgba(49, 51, 63, 0.16);
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 12px;
        background: #fafafa;
    }
    .indicator-title {
        font-size: 1.02rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .indicator-desc {
        font-size: 0.93rem;
        margin-bottom: 0.5rem;
    }
    .small-label {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #555;
        letter-spacing: 0.03em;
    }
    .small-text {
        font-size: 0.88rem;
        margin-bottom: 0.35rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

rows = [
    # CONTEXT
    {
        'section': 'Context',
        'group': 'Population structure and ageing',
        'indicator': 'Population age structure',
        'description': 'Population by age classes. General demographic context for Bergamo, Lombardia, and Italy.',
        'source': 'ISTAT Demo / demographic indicators',
        'province': 'Yes',
        'graphic': 'Population pyramid or stacked age bars',
    },
    {
        'section': 'Context',
        'group': 'Population structure and ageing',
        'indicator': 'Net migration by age',
        'description': 'Migration balance by age class. Useful to see whether young adults are gained or lost.',
        'source': 'ISTAT Demo / demographic indicators',
        'province': 'Partly yes',
        'graphic': 'Age profile line or diverging bars',
    },
    {
        'section': 'Context',
        'group': 'Population structure and ageing',
        'indicator': 'Old-age dependency ratio (OADR)',
        'description': 'Population aged 65+ relative to population aged 15-64.',
        'source': 'ISTAT Demo / demographic indicators',
        'province': 'Yes',
        'graphic': 'Simple trend line',
    },
    {
        'section': 'Context',
        'group': 'Population structure and ageing',
        'indicator': 'Ageing index',
        'description': 'Population aged 65+ relative to population aged 0-14.',
        'source': 'ISTAT Demo / demographic indicators',
        'province': 'Yes',
        'graphic': 'Simple trend line',
    },
    {
        'section': 'Context',
        'group': 'Population structure and ageing',
        'indicator': 'Mean age',
        'description': 'Average age of the resident population.',
        'source': 'ISTAT Demo / demographic indicators',
        'province': 'Yes',
        'graphic': 'Lollipop chart across territories',
    },
    {
        'section': 'Context',
        'group': 'Population structure and ageing',
        'indicator': 'Share aged 80+',
        'description': 'Weight of very old population in the local age structure.',
        'source': 'ISTAT Demo / demographic indicators',
        'province': 'Yes',
        'graphic': 'Bar chart across territories',
    },
    # CORE YOUTH
    {
        'section': 'Core youth section',
        'group': 'Education and training',
        'indicator': 'Tertiary attainment (%)',
        'description': 'Share of people aged 25-34 with tertiary education. We can split by sex.',
        'source': 'Eurostat',
        'province': 'No, not standard',
        'graphic': 'Trend line and last-year comparison',
    },
    {
        'section': 'Core youth section',
        'group': 'Education and training',
        'indicator': 'Tertiary attainment (absolute number)',
        'description': 'Estimated number of people aged 25-34 with tertiary education. Built as rate × population.',
        'source': 'Eurostat + population data',
        'province': 'No, not standard',
        'graphic': 'Bar chart across territories',
    },
    {
        'section': 'Core youth section',
        'group': 'Youth employment and job quality',
        'indicator': 'Employment rate after education',
        'description': 'Employment rate of young people not in education, by education level and years since completion.',
        'source': 'Eurostat',
        'province': 'No, NUTS2 yes',
        'graphic': 'Grouped line chart by years since completion',
    },
    {
        'section': 'Core youth section',
        'group': 'Youth employment and job quality',
        'indicator': 'NEET rate',
        'description': 'Young people not in employment, education, or training. Can be split by sex.',
        'source': 'Eurostat',
        'province': 'No, NUTS2 yes',
        'graphic': 'Trend line and last-year comparison',
    },
    {
        'section': 'Core youth section',
        'group': 'Mobility and retention',
        'indicator': 'Youth mobility balance',
        'description': 'Net balance of young people entering and leaving the territory.',
        'source': 'ISTAT',
        'province': 'Yes, age detail to verify',
        'graphic': 'Bar chart or line over time',
    },
    {
        'section': 'Core youth section',
        'group': 'Housing and well-being',
        'indicator': 'Housing burden / housing stress proxy',
        'description': 'Indicator of housing cost pressure or housing-related vulnerability.',
        'source': 'BES / ISTAT BesT',
        'province': 'Often yes',
        'graphic': 'Lollipop chart across territories',
    },
    {
        'section': 'Core youth section',
        'group': 'Housing and well-being',
        'indicator': 'Subjective well-being',
        'description': 'Summary measure of satisfaction or subjective well-being.',
        'source': 'BES / ISTAT BesT',
        'province': 'Often yes',
        'graphic': 'Bar chart across territories',
    },
    {
        'section': 'Core youth section',
        'group': 'Housing and well-being',
        'indicator': 'Confidence in the future / perceived stability',
        'description': 'Where available, an indicator of expectations or perceived economic and life stability.',
        'source': 'BES, to verify',
        'province': 'To verify',
        'graphic': 'Bar chart across territories',
    },
    {
        'section': 'Core youth section',
        'group': 'Demographic projections of labour-market entry',
        'indicator': 'Entry cohorts index (19)',
        'description': 'Projected number or index of people reaching age 19.',
        'source': 'ISTAT demographic projections',
        'province': 'Region yes; province not immediate',
        'graphic': 'Projection line',
    },
    {
        'section': 'Core youth section',
        'group': 'Demographic projections of labour-market entry',
        'indicator': 'Entry cohorts index (21)',
        'description': 'Projected number or index of people reaching age 21.',
        'source': 'ISTAT demographic projections',
        'province': 'Region yes; province not immediate',
        'graphic': 'Projection line',
    },
    {
        'section': 'Core youth section',
        'group': 'Demographic projections of labour-market entry',
        'indicator': 'Entry cohorts index (25)',
        'description': 'Projected number or index of people reaching age 25.',
        'source': 'ISTAT demographic projections',
        'province': 'Region yes; province not immediate',
        'graphic': 'Projection line',
    },
]

df = pd.DataFrame(rows)

st.title('HEYE Dashboard - Indicator Catalog')
st.caption('Prototype page for the meeting: this does not show final values yet. It shows sections, indicators, metadata, and the chart style planned for each block.')

with st.sidebar:
    st.header('Filters')
    section_filter = st.multiselect('Section', sorted(df['section'].unique()), default=sorted(df['section'].unique()))
    group_filter = st.multiselect('Group', sorted(df['group'].unique()), default=sorted(df['group'].unique()))
    provincial_only = st.toggle('Show only indicators already possible at provincial level', value=False)
    st.markdown('---')
    st.markdown('**Legend**')
    st.write('This page is meant to show how the dashboard will be organized before we plug in the final data files.')

view = df[df['section'].isin(section_filter) & df['group'].isin(group_filter)].copy()
if provincial_only:
    view = view[view['province'].str.startswith('Yes')]

# Summary block
c1, c2, c3, c4 = st.columns(4)
c1.metric('Indicators selected', len(view))
c2.metric('Sections', view['section'].nunique())
c3.metric('Groups', view['group'].nunique())
c4.metric('Already provincial', int(view['province'].str.startswith('Yes').sum()))

st.markdown('---')

# Quick table for meeting notes
st.subheader('Compact schema')
compact = view[['indicator', 'description', 'source', 'province']].rename(columns={
    'indicator': 'Indicator',
    'description': 'Very short description',
    'source': 'Data source',
    'province': 'Provincial level already possible?'
})
st.dataframe(compact, use_container_width=True, hide_index=True)

st.markdown('---')

# Visual catalog by section/group
for section in view['section'].unique():
    st.header(section)
    section_df = view[view['section'] == section]
    for group in section_df['group'].unique():
        st.subheader(group)
        group_df = section_df[section_df['group'] == group]
        cols = st.columns(2)
        for i, (_, row) in enumerate(group_df.iterrows()):
            with cols[i % 2]:
                st.markdown(
                    f"""
                    <div class='indicator-card'>
                        <div class='indicator-title'>{row['indicator']}</div>
                        <div class='indicator-desc'>{row['description']}</div>
                        <div class='small-label'>Data source</div>
                        <div class='small-text'>{row['source']}</div>
                        <div class='small-label'>Provincial level already possible?</div>
                        <div class='small-text'>{row['province']}</div>
                        <div class='small-label'>Planned chart</div>
                        <div class='small-text'>{row['graphic']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                # small placeholder visual
                placeholder = pd.DataFrame({
                    'Bergamo': [62, 65, 68],
                    'Lombardia': [60, 63, 66],
                    'Italia': [56, 58, 60],
                }, index=['2022', '2023', '2024'])
                if 'Projection' in row['graphic'] or 'line' in row['graphic'].lower() or 'Trend' in row['graphic']:
                    st.line_chart(placeholder)
                elif 'Bar' in row['graphic'] or 'bar' in row['graphic']:
                    st.bar_chart(placeholder.iloc[-1])
                elif 'pyramid' in row['graphic'].lower() or 'stacked' in row['graphic'].lower():
                    demo = pd.DataFrame({
                        'Age class': ['0-14', '15-24', '25-34', '35-49', '50-64', '65+'],
                        'Share': [12, 10, 11, 19, 22, 26]
                    }).set_index('Age class')
                    st.bar_chart(demo)
                else:
                    st.area_chart(placeholder)

st.markdown('---')
st.subheader('Notes for the next step')
st.markdown(
    """
- Once we decide the final set, each indicator can be linked to one file and one chart page.
- The compact schema above can be exported to Excel if needed.
- The placeholder charts are only there to show the graphical logic during the meeting.
    """
)
