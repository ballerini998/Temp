import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title='HEYE Dashboard Blueprint', layout='wide')

st.title('HEYE Dashboard Blueprint')
st.caption('Prototype of the dashboard structure, indicators, sources, and expected visual layout')

rows = [
    {
        'Section': 'Context and demography',
        'Indicator': 'Age structure of the population',
        'Description': 'Population by age groups; demographic context for Bergamo, Lombardia, and Italy.',
        'Source': 'ISTAT Demo / PPC',
        'Provincial level already available?': True,
        'Planned chart': 'Population pyramid / grouped bars',
    },
    {
        'Section': 'Context and demography',
        'Indicator': 'International migration balance',
        'Description': 'International migration balance by age or age group; useful to see whether young people are gained or lost from abroad.',
        'Source': 'ISTAT Demo + ISTAT Esplora Dati (migrations)',
        'Provincial level already available?': True,
        'Planned chart': 'Age profile line / bars',
    },
    {
        'Section': 'Context and demography',
        'Indicator': 'Internal migration balance',
        'Description': 'Internal migration balance across Italian territories; useful even when moves stay inside the broader local community.',
        'Source': 'ISTAT Esplora Dati (migrations)',
        'Provincial level already available?': False,
        'Planned chart': 'Age profile line / bars',
    },
    {
        'Section': 'Context and demography',
        'Indicator': 'Old-age dependency ratio (OADR)',
        'Description': 'Population aged 65+ relative to population aged 15–64.',
        'Source': 'ISTAT Demo / PPC',
        'Provincial level already available?': True,
        'Planned chart': 'Trend line',
    },
    {
        'Section': 'Context and demography',
        'Indicator': 'Ageing index',
        'Description': 'Population aged 65+ relative to population aged 0–14.',
        'Source': 'ISTAT Demo / PPC',
        'Provincial level already available?': True,
        'Planned chart': 'Trend line',
    },
    {
        'Section': 'Context and demography',
        'Indicator': 'Mean age',
        'Description': 'Average age of the resident population.',
        'Source': 'ISTAT Demo / PPC',
        'Provincial level already available?': True,
        'Planned chart': 'Dot plot / trend line',
    },
    {
        'Section': 'Context and demography',
        'Indicator': 'Share aged 80+',
        'Description': 'Weight of the oldest-old population in the territory.',
        'Source': 'ISTAT Demo / PPC',
        'Provincial level already available?': True,
        'Planned chart': 'Trend line',
    },
    {
        'Section': 'Core youth indicators',
        'Indicator': 'Tertiary attainment (%)',
        'Description': 'Tertiary education profile using university-level data; can be shown by sex and treated as local/provincial through the ateneo.',
        'Source': 'USTAT MUR + national context data where needed',
        'Provincial level already available?': True,
        'Planned chart': 'Grouped bars by territory and sex',
    },
    {
        'Section': 'Core youth indicators',
        'Indicator': 'Tertiary attainment (absolute number)',
        'Description': 'Absolute number linked to the local tertiary education pipeline using university-level data.',
        'Source': 'USTAT MUR + national context data where needed',
        'Provincial level already available?': True,
        'Planned chart': 'Bars / line trend',
    },
    {
        'Section': 'Core youth indicators',
        'Indicator': 'University enrolments',
        'Description': 'Students enrolled in university; can be shown by institution and sex.',
        'Source': 'USTAT MUR',
        'Provincial level already available?': True,
        'Planned chart': 'Bars by institution / trend line',
    },
    {
        'Section': 'Core youth indicators',
        'Indicator': 'University first-year entrants',
        'Description': 'New entrants to university, useful to track the local educational pipeline.',
        'Source': 'USTAT MUR',
        'Provincial level already available?': True,
        'Planned chart': 'Bars / line trend',
    },
    {
        'Section': 'Core youth indicators',
        'Indicator': 'University graduates',
        'Description': 'Number of graduates; useful to profile local tertiary education output.',
        'Source': 'USTAT MUR',
        'Provincial level already available?': True,
        'Planned chart': 'Bars / line trend',
    },
    {
        'Section': 'Core youth indicators',
        'Indicator': 'ITS enrolments / diplomas',
        'Description': 'Students enrolled in ITS Academy and diploma outcomes where territorial detail is available.',
        'Source': 'INDIRE ITS Academy monitoring',
        'Provincial level already available?': True,
        'Planned chart': 'Bars / KPI cards',
    },
    {
        'Section': 'Core youth indicators',
        'Indicator': 'Youth employment rate',
        'Description': 'Employment rate of young people; can be separated by sex and sometimes by education.',
        'Source': 'ISTAT Esplora Dati + Eurostat',
        'Provincial level already available?': True,
        'Planned chart': 'Grouped bars / trend line',
    },
    {
        'Section': 'Core youth indicators',
        'Indicator': 'Employment rate of young non-students by education and years since completion',
        'Description': 'Employment of young people no longer in education, by attainment level and years since completion.',
        'Source': 'Eurostat; Labour Force Survey may offer additional Italian detail',
        'Provincial level already available?': False,
        'Planned chart': 'Multi-line chart',
    },
    {
        'Section': 'Core youth indicators',
        'Indicator': 'NEET rate',
        'Description': 'Young people not in employment, education or training; separated by sex where available.',
        'Source': 'Eurostat',
        'Provincial level already available?': False,
        'Planned chart': 'Grouped bars / trend line',
    },
    {
        'Section': 'Core youth indicators',
        'Indicator': 'Inactive youth',
        'Description': 'Inactive young people outside the labour force; useful to complement employment and NEET.',
        'Source': 'ISTAT Esplora Dati',
        'Provincial level already available?': True,
        'Planned chart': 'Bars / trend line',
    },
    {
        'Section': 'Core youth indicators',
        'Indicator': 'Housing burden / housing stress',
        'Description': 'Proxy of economic pressure from housing costs.',
        'Source': 'ISTAT BesT',
        'Provincial level already available?': True,
        'Planned chart': 'Bars / dot plot',
    },
    {
        'Section': 'Core youth indicators',
        'Indicator': 'Subjective well-being',
        'Description': 'Indicator of life satisfaction or subjective well-being; can be split by sex where available.',
        'Source': 'ISTAT BesT',
        'Provincial level already available?': True,
        'Planned chart': 'Bars / dot plot',
    },
    {
        'Section': 'Core youth indicators',
        'Indicator': 'Entry cohorts index (19, 21, 25)',
        'Description': 'Number and index of cohorts reaching ages 19, 21, and 25 under demographic projections.',
        'Source': 'ISTAT Demo / PPC',
        'Provincial level already available?': True,
        'Planned chart': 'Indexed trend lines',
    },
]

df = pd.DataFrame(rows)
df['Provincial availability'] = df['Provincial level already available?'].map(lambda x: '✅' if x else '')

with st.sidebar:
    st.header('Filters')
    section = st.multiselect('Section', options=df['Section'].unique(), default=list(df['Section'].unique()))
    only_nonprov = st.checkbox('Show only indicators without provincial availability', value=False)
    st.markdown('---')
    st.markdown('**Reading rule**')
    st.write('Ateneo-level indicators are treated as equivalent to provincial/local availability.')

fdf = df[df['Section'].isin(section)].copy()
if only_nonprov:
    fdf = fdf[~fdf['Provincial level already available?']]

st.subheader('Operational schema')
display_df = fdf[[
    'Section', 'Indicator', 'Description', 'Source', 'Provincial availability'
]].rename(columns={'Provincial availability': 'Provincial level already available?'})
st.dataframe(display_df, use_container_width=True, hide_index=True)

csv = display_df.to_csv(index=False).encode('utf-8')
st.download_button('Download schema as CSV', csv, file_name='heye_dashboard_schema.csv', mime='text/csv')

preview_map = {
    'Population pyramid / grouped bars': pd.DataFrame({'Group': ['0-14', '15-24', '25-34', '35-64', '65+'], 'Bergamo': [11, 10, 12, 42, 25]}),
    'Age profile line / bars': pd.DataFrame({'Age': [15, 20, 25, 30, 35], 'Balance': [-1, 3, 7, 2, -2]}),
    'Trend line': pd.DataFrame({'Year': [2020, 2025, 2030, 2035, 2040], 'Value': [100, 104, 109, 113, 118]}),
    'Dot plot / trend line': pd.DataFrame({'Territory': ['Bergamo', 'Lombardia', 'Italia'], 'Value': [45.2, 46.8, 47.9]}),
    'Grouped bars by territory and sex': pd.DataFrame({'Territory': ['Bergamo', 'Bergamo', 'Lombardia', 'Lombardia', 'Italia', 'Italia'], 'Sex': ['F', 'M', 'F', 'M', 'F', 'M'], 'Value': [38, 32, 41, 35, 39, 33]}),
    'Bars / line trend': pd.DataFrame({'Year': [2018, 2019, 2020, 2021, 2022], 'Value': [80, 83, 78, 85, 88]}),
    'Bars by institution / trend line': pd.DataFrame({'Institution': ['UniBg', 'Milano', 'Brescia'], 'Value': [17000, 61000, 15000]}),
    'Bars / KPI cards': pd.DataFrame({'Category': ['Enrolled', 'Graduates'], 'Value': [1200, 850]}),
    'Grouped bars / trend line': pd.DataFrame({'Territory': ['Bergamo', 'Lombardia', 'Italia'], 'Value': [61, 64, 58]}),
    'Multi-line chart': pd.DataFrame({'Years': [1, 2, 3, 4], 'Low edu': [52, 57, 60, 62], 'Medium edu': [68, 72, 74, 76], 'High edu': [79, 83, 85, 87]}),
    'Bars / dot plot': pd.DataFrame({'Territory': ['Bergamo', 'Lombardia', 'Italia'], 'Value': [22, 19, 24]}),
    'Indexed trend lines': pd.DataFrame({'Year': [2024, 2026, 2028, 2030, 2032], 'Age 19': [100, 98, 95, 92, 89], 'Age 21': [100, 99, 97, 94, 91], 'Age 25': [100, 101, 100, 98, 95]}),
}

st.subheader('Visual preview by section')
for sec in fdf['Section'].unique():
    st.markdown(f'## {sec}')
    sdf = fdf[fdf['Section'] == sec]
    for _, r in sdf.iterrows():
        with st.container(border=True):
            c1, c2 = st.columns([1.3, 1])
            with c1:
                st.markdown(f"### {r['Indicator']}")
                st.write(r['Description'])
                st.markdown(f"**Source:** {r['Source']}")
                st.markdown(f"**Provincial level already available?** {'✅' if r['Provincial level already available?'] else ''}")
                st.markdown(f"**Planned chart:** {r['Planned chart']}")
            with c2:
                pdata = preview_map.get(r['Planned chart'])
                if pdata is None:
                    st.info('Preview not available')
                else:
                    chart_type = r['Planned chart']
                    if chart_type == 'Population pyramid / grouped bars':
                        long = pdata.melt(id_vars='Group', var_name='Territory', value_name='Value')
                        chart = alt.Chart(long).mark_bar().encode(x='Group:N', y='Value:Q', color='Territory:N')
                    elif chart_type == 'Age profile line / bars':
                        chart = alt.Chart(pdata).mark_line(point=True).encode(x='Age:Q', y='Balance:Q')
                    elif chart_type in ['Trend line', 'Bars / line trend', 'Indexed trend lines']:
                        if chart_type == 'Indexed trend lines':
                            long = pdata.melt(id_vars='Year', var_name='Series', value_name='Value')
                            chart = alt.Chart(long).mark_line(point=True).encode(x='Year:Q', y='Value:Q', color='Series:N')
                        else:
                            chart = alt.Chart(pdata).mark_line(point=True).encode(x=list(pdata.columns)[0]+':Q', y='Value:Q')
                    elif chart_type in ['Dot plot / trend line', 'Bars / dot plot', 'Grouped bars / trend line']:
                        chart = alt.Chart(pdata).mark_bar().encode(x='Territory:N', y='Value:Q')
                    elif chart_type == 'Grouped bars by territory and sex':
                        chart = alt.Chart(pdata).mark_bar().encode(x='Territory:N', y='Value:Q', color='Sex:N', xOffset='Sex:N')
                    elif chart_type == 'Bars by institution / trend line':
                        chart = alt.Chart(pdata).mark_bar().encode(x='Institution:N', y='Value:Q')
                    elif chart_type == 'Bars / KPI cards':
                        chart = alt.Chart(pdata).mark_bar().encode(x='Category:N', y='Value:Q')
                    elif chart_type == 'Multi-line chart':
                        long = pdata.melt(id_vars='Years', var_name='Education', value_name='Value')
                        chart = alt.Chart(long).mark_line(point=True).encode(x='Years:Q', y='Value:Q', color='Education:N')
                    else:
                        chart = alt.Chart(pdata).mark_bar().encode(x=list(pdata.columns)[0]+':N', y='Value:Q')
                    st.altair_chart(chart.properties(height=220), use_container_width=True)
