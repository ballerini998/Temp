import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title='HEYE Dashboard Blueprint', layout='wide')

# ----------------------------
# Metadata
# ----------------------------
INDICATORS = [
    # Presentation schema rows
    {
        'section': 'Context and demography',
        'indicator': 'Age structure of the population',
        'description': 'Population by age groups. Graph preview shown for Total, Female, and Male, with Bergamo, Lombardia, and Italy.',
        'source': 'ISTAT Demo / PPC',
        'provincial': True,
        'territories': ['Bergamo', 'Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'age_structure',
    },
    {
        'section': 'Context and demography',
        'indicator': 'International migration balance',
        'description': 'Migration balance from abroad by age group. Preview shown for Total, Female, and Male, with Bergamo, Lombardia, and Italy.',
        'source': 'ISTAT Demo + ISTAT Esplora Dati',
        'provincial': True,
        'territories': ['Bergamo', 'Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'migration_balance',
    },
    {
        'section': 'Context and demography',
        'indicator': 'Internal migration balance',
        'description': 'Internal migration balance. Preview shown for Lombardia and Italy only, because provincial availability is not part of the core plan.',
        'source': 'ISTAT Esplora Dati',
        'provincial': False,
        'territories': ['Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'migration_balance',
    },
    {
        'section': 'Context and demography',
        'indicator': 'Old-age dependency ratio (OADR)',
        'description': 'Population aged 65+ relative to population aged 15–64. No Male/Female split in the preview because it is not the most meaningful choice here.',
        'source': 'ISTAT Demo / PPC',
        'provincial': True,
        'territories': ['Bergamo', 'Lombardia', 'Italia'],
        'sex_split': False,
        'chart': 'trend',
    },
    {
        'section': 'Context and demography',
        'indicator': 'Ageing index',
        'description': 'Population aged 65+ relative to population aged 0–14. Preview shown for Total, Female, and Male, with Bergamo, Lombardia, and Italy.',
        'source': 'ISTAT Demo / PPC',
        'provincial': True,
        'territories': ['Bergamo', 'Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'trend',
    },
    {
        'section': 'Context and demography',
        'indicator': 'Mean age',
        'description': 'Average age of the resident population. Preview shown for Total, Female, and Male, with Bergamo, Lombardia, and Italy.',
        'source': 'ISTAT Demo / PPC',
        'provincial': True,
        'territories': ['Bergamo', 'Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'trend',
    },
    {
        'section': 'Context and demography',
        'indicator': 'Share aged 80+',
        'description': 'Weight of the oldest-old population. Preview shown for Total, Female, and Male, with Bergamo, Lombardia, and Italy.',
        'source': 'ISTAT Demo / PPC',
        'provincial': True,
        'territories': ['Bergamo', 'Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'trend',
    },
    {
        'section': 'Education and training',
        'indicator': 'Tertiary attainment (%)',
        'description': 'Tertiary education profile using ateneo-level data. Ateneo is treated as local/provincial availability. Preview shown for Total, Female, and Male.',
        'source': 'USTAT MUR + national context data if needed',
        'provincial': True,
        'territories': ['Bergamo', 'Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'bars_territory_sex',
    },
    {
        'section': 'Education and training',
        'indicator': 'Tertiary attainment (absolute number)',
        'description': 'Absolute number linked to the local tertiary education pipeline. Preview shown for Total, Female, and Male.',
        'source': 'USTAT MUR + national context data if needed',
        'provincial': True,
        'territories': ['Bergamo', 'Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'bars_territory_sex',
    },
    {
        'section': 'Education and training',
        'indicator': 'University enrolments',
        'description': 'Students enrolled in university. Preview shown for Total, Female, and Male, with Bergamo, Lombardia, and Italy.',
        'source': 'USTAT MUR',
        'provincial': True,
        'territories': ['Bergamo', 'Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'bars_territory_sex',
    },
    {
        'section': 'Education and training',
        'indicator': 'University first-year entrants',
        'description': 'New university entrants. Preview shown for Total, Female, and Male, with Bergamo, Lombardia, and Italy.',
        'source': 'USTAT MUR',
        'provincial': True,
        'territories': ['Bergamo', 'Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'bars_territory_sex',
    },
    {
        'section': 'Education and training',
        'indicator': 'University graduates',
        'description': 'Number of graduates. Preview shown for Total, Female, and Male, with Bergamo, Lombardia, and Italy.',
        'source': 'USTAT MUR',
        'provincial': True,
        'territories': ['Bergamo', 'Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'bars_territory_sex',
    },
    {
        'section': 'Education and training',
        'indicator': 'ITS enrolments / diplomas',
        'description': 'ITS Academy enrolments and diplomas where territorial detail is available. Preview shown for Total, Female, and Male.',
        'source': 'INDIRE ITS Academy monitoring',
        'provincial': True,
        'territories': ['Bergamo', 'Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'bars_territory_sex',
    },
    {
        'section': 'Youth employment and job quality',
        'indicator': 'Youth employment rate',
        'description': 'General youth employment rate. Preview shown for Total, Female, and Male, with Bergamo, Lombardia, and Italy.',
        'source': 'ISTAT Esplora Dati + Eurostat',
        'provincial': True,
        'territories': ['Bergamo', 'Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'bars_territory_sex',
    },
    {
        'section': 'Youth employment and job quality',
        'indicator': 'Employment rate of young non-students by education and years since completion',
        'description': 'Employment of young people no longer in education, by attainment level and years since completion. Preview shown only for Lombardia and Italy.',
        'source': 'Eurostat; Labour Force Survey may add Italian detail',
        'provincial': False,
        'territories': ['Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'education_years_since',
    },
    {
        'section': 'Youth employment and job quality',
        'indicator': 'NEET rate',
        'description': 'Young people not in employment, education, or training. Preview shown only for Lombardia and Italy.',
        'source': 'Eurostat',
        'provincial': False,
        'territories': ['Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'bars_territory_sex',
    },
    {
        'section': 'Youth employment and job quality',
        'indicator': 'Inactive youth',
        'description': 'Inactive young people outside the labour force. Preview shown for Total, Female, and Male, with Bergamo, Lombardia, and Italy.',
        'source': 'ISTAT Esplora Dati',
        'provincial': True,
        'territories': ['Bergamo', 'Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'bars_territory_sex',
    },
    {
        'section': 'Mobility and retention',
        'indicator': 'International migration balance',
        'description': 'International migration balance for the youth focus. Preview shown for Total, Female, and Male, with Bergamo, Lombardia, and Italy.',
        'source': 'ISTAT Demo + ISTAT Esplora Dati',
        'provincial': True,
        'territories': ['Bergamo', 'Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'migration_balance',
    },
    {
        'section': 'Mobility and retention',
        'indicator': 'Internal migration balance',
        'description': 'Internal migration balance. Preview shown only for Lombardia and Italy.',
        'source': 'ISTAT Esplora Dati',
        'provincial': False,
        'territories': ['Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'migration_balance',
    },
    {
        'section': 'Housing and well-being',
        'indicator': 'Housing burden / housing stress',
        'description': 'Proxy of economic pressure from housing costs. Preview shown for Total, Female, and Male, with Bergamo, Lombardia, and Italy.',
        'source': 'ISTAT BesT',
        'provincial': True,
        'territories': ['Bergamo', 'Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'bars_territory_sex',
    },
    {
        'section': 'Housing and well-being',
        'indicator': 'Subjective well-being',
        'description': 'Life satisfaction or subjective well-being. Preview shown for Total, Female, and Male, with Bergamo, Lombardia, and Italy.',
        'source': 'ISTAT BesT',
        'provincial': True,
        'territories': ['Bergamo', 'Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'bars_territory_sex',
    },
    {
        'section': 'Demographic projections of labour-market entry',
        'indicator': 'Entry cohorts index (19, 21, 25)',
        'description': 'Number and index of cohorts reaching ages 19, 21, and 25. Preview shown for Bergamo, Lombardia, and Italy.',
        'source': 'ISTAT Demo / PPC',
        'provincial': True,
        'territories': ['Bergamo', 'Lombardia', 'Italia'],
        'sex_split': True,
        'chart': 'entry_cohorts',
    },
]

sections_order = [
    'Presentation / operational schema',
    'Context and demography',
    'Education and training',
    'Youth employment and job quality',
    'Mobility and retention',
    'Housing and well-being',
    'Demographic projections of labour-market entry',
]

schema_df = pd.DataFrame(INDICATORS)
schema_df['Provincial availability'] = schema_df['provincial'].map(lambda x: '✅' if x else '')
schema_df_display = schema_df[['section', 'indicator', 'description', 'source', 'Provincial availability']].rename(columns={
    'section': 'Section',
    'indicator': 'Indicator',
    'description': 'Description',
    'source': 'Source',
    'Provincial availability': 'Provincial level already available?'
})

# ----------------------------
# Placeholder data generators
# ----------------------------
def territory_sex_values(territories):
    rows = []
    base = {'Bergamo': 62, 'Lombardia': 66, 'Italia': 59}
    shift = {'Total': 0, 'Female': -4, 'Male': 3}
    for t in territories:
        for s in ['Total', 'Female', 'Male']:
            val = base.get(t, 60) + shift[s]
            rows.append({'Territory': t, 'Sex': s, 'Value': val})
    return pd.DataFrame(rows)


def trend_values(territories, sex_split=True):
    years = [2018, 2020, 2022, 2024, 2026]
    rows = []
    tbase = {'Bergamo': 100, 'Lombardia': 103, 'Italia': 98}
    sshift = {'Total': 0, 'Female': 2, 'Male': -1}
    for t in territories:
        sexes = ['Total', 'Female', 'Male'] if sex_split else ['Total']
        for s in sexes:
            for i, y in enumerate(years):
                rows.append({'Year': y, 'Territory': t, 'Sex': s, 'Value': tbase.get(t, 100) + i*2 + sshift.get(s, 0)})
    return pd.DataFrame(rows)


def age_structure_values(territories):
    age_groups = ['0-14', '15-24', '25-34', '35-64', '65+']
    rows = []
    profile = {
        'Bergamo': [12, 10, 12, 42, 24],
        'Lombardia': [12, 10, 13, 41, 24],
        'Italia': [12, 9, 11, 41, 27],
    }
    sex_adj = {'Total': [0,0,0,0,0], 'Female': [0,0,-1,-1,2], 'Male': [0,0,1,1,-2]}
    for t in territories:
        for s in ['Total', 'Female', 'Male']:
            for ag, v, adj in zip(age_groups, profile.get(t, profile['Italia']), sex_adj[s]):
                rows.append({'Territory': t, 'Sex': s, 'Age group': ag, 'Value': v + adj})
    return pd.DataFrame(rows)


def migration_values(territories):
    age_groups = ['15-19', '20-24', '25-29', '30-34']
    base = {'Bergamo': [1, 5, 7, 3], 'Lombardia': [2, 6, 8, 4], 'Italia': [0, 2, 3, 1]}
    sex_adj = {'Total': 0, 'Female': -1, 'Male': 1}
    rows = []
    for t in territories:
        for s in ['Total', 'Female', 'Male']:
            for ag, v in zip(age_groups, base.get(t, base['Italia'])):
                rows.append({'Territory': t, 'Sex': s, 'Age group': ag, 'Value': v + sex_adj[s]})
    return pd.DataFrame(rows)


def education_years_values(territories):
    years_since = [1, 2, 3, 4, 5]
    educations = ['Low', 'Medium', 'High']
    rows = []
    terr_adj = {'Lombardia': 2, 'Italia': 0}
    sex_adj = {'Total': 0, 'Female': -3, 'Male': 2}
    edu_base = {'Low': 55, 'Medium': 68, 'High': 79}
    for t in territories:
        for s in ['Total', 'Female', 'Male']:
            for e in educations:
                for i, ys in enumerate(years_since):
                    rows.append({'Territory': t, 'Sex': s, 'Years since completion': ys, 'Education': e,
                                 'Value': edu_base[e] + i*2 + terr_adj.get(t, 0) + sex_adj[s]})
    return pd.DataFrame(rows)


def entry_cohorts_values(territories):
    years = [2024, 2026, 2028, 2030, 2032]
    ages = ['19', '21', '25']
    base = {
        'Bergamo': {'19': 100, '21': 100, '25': 100},
        'Lombardia': {'19': 100, '21': 101, '25': 102},
        'Italia': {'19': 100, '21': 99, '25': 98},
    }
    sex_adj = {'Total': 0, 'Female': -1, 'Male': 1}
    rows = []
    for t in territories:
        for s in ['Total', 'Female', 'Male']:
            for age in ages:
                for i, y in enumerate(years):
                    rows.append({'Year': y, 'Territory': t, 'Sex': s, 'Entry age': age,
                                 'Value': base[t][age] - i*(2 if age=='19' else 1 if age=='21' else 0.5) + sex_adj[s]})
    return pd.DataFrame(rows)

# ----------------------------
# Chart renderers
# ----------------------------
def render_basic_bar(ind):
    df = territory_sex_values(ind['territories'])
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Territory:N', title='Territory'),
        y=alt.Y('Value:Q', title='Value'),
        color=alt.Color('Sex:N', title='Sex'),
        xOffset='Sex:N',
        tooltip=['Territory', 'Sex', 'Value']
    )
    st.altair_chart(chart.properties(height=320), use_container_width=True)


def render_trend(ind):
    df = trend_values(ind['territories'], sex_split=ind['sex_split'])
    if ind['sex_split']:
        sex_choice = st.radio('Sex', ['Total', 'Female', 'Male'], horizontal=True, key=f"sex_{ind['indicator']}")
        df = df[df['Sex'] == sex_choice]
    chart = alt.Chart(df).mark_line(point=True).encode(
        x='Year:Q',
        y='Value:Q',
        color='Territory:N',
        tooltip=['Year', 'Territory', 'Value']
    )
    st.altair_chart(chart.properties(height=320), use_container_width=True)


def render_age_structure(ind):
    df = age_structure_values(ind['territories'])
    sex_choice = st.radio('Sex', ['Total', 'Female', 'Male'], horizontal=True, key=f"sex_{ind['indicator']}")
    df = df[df['Sex'] == sex_choice]
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Age group:N', title='Age group'),
        y=alt.Y('Value:Q', title='Share / value'),
        color='Territory:N',
        xOffset='Territory:N',
        tooltip=['Age group', 'Territory', 'Value']
    )
    st.altair_chart(chart.properties(height=320), use_container_width=True)


def render_migration(ind):
    df = migration_values(ind['territories'])
    sex_choice = st.radio('Sex', ['Total', 'Female', 'Male'], horizontal=True, key=f"sex_{ind['indicator']}")
    df = df[df['Sex'] == sex_choice]
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Age group:N', title='Age group'),
        y=alt.Y('Value:Q', title='Migration balance'),
        color='Territory:N',
        xOffset='Territory:N',
        tooltip=['Age group', 'Territory', 'Value']
    )
    st.altair_chart(chart.properties(height=320), use_container_width=True)


def render_education_years(ind):
    df = education_years_values(ind['territories'])
    sex_choice = st.radio('Sex', ['Total', 'Female', 'Male'], horizontal=True, key=f"sex_{ind['indicator']}")
    df = df[df['Sex'] == sex_choice]
    territory_choice = st.radio('Territory', ind['territories'], horizontal=True, key=f"terr_{ind['indicator']}")
    df = df[df['Territory'] == territory_choice]
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('Years since completion:Q', title='Years since completion'),
        y=alt.Y('Value:Q', title='Employment rate'),
        color='Education:N',
        tooltip=['Years since completion', 'Education', 'Value']
    )
    st.altair_chart(chart.properties(height=320), use_container_width=True)


def render_entry_cohorts(ind):
    df = entry_cohorts_values(ind['territories'])
    sex_choice = st.radio('Sex', ['Total', 'Female', 'Male'], horizontal=True, key=f"sex_{ind['indicator']}")
    df = df[df['Sex'] == sex_choice]
    age_choice = st.radio('Entry age', ['19', '21', '25'], horizontal=True, key=f"age_{ind['indicator']}")
    df = df[df['Entry age'] == age_choice]
    chart = alt.Chart(df).mark_line(point=True).encode(
        x='Year:Q',
        y=alt.Y('Value:Q', title='Index / count'),
        color='Territory:N',
        tooltip=['Year', 'Territory', 'Value']
    )
    st.altair_chart(chart.properties(height=320), use_container_width=True)


def render_indicator(ind):
    st.markdown(f"### {ind['indicator']}")
    st.write(ind['description'])
    meta1, meta2 = st.columns([2, 1])
    with meta1:
        st.markdown(f"**Source:** {ind['source']}")
        st.markdown(f"**Territories in preview:** {', '.join(ind['territories'])}")
    with meta2:
        st.markdown(f"**Provincial available:** {'✅' if ind['provincial'] else ''}")
        st.markdown(f"**Sex split in preview:** {'Yes' if ind['sex_split'] else 'No'}")

    chart = ind['chart']
    if chart == 'bars_territory_sex':
        render_basic_bar(ind)
    elif chart == 'trend':
        render_trend(ind)
    elif chart == 'age_structure':
        render_age_structure(ind)
    elif chart == 'migration_balance':
        render_migration(ind)
    elif chart == 'education_years_since':
        render_education_years(ind)
    elif chart == 'entry_cohorts':
        render_entry_cohorts(ind)

# ----------------------------
# App layout
# ----------------------------
st.title('HEYE Dashboard Blueprint')
st.caption('Operational schema plus visual preview of the future dashboard with placeholder data')

with st.sidebar:
    st.header('Menu')
    page = st.radio('Go to', sections_order)
    st.markdown('---')
    st.markdown('**Rule used in this prototype**')
    st.write('Ateneo-level indicators are treated as equivalent to provincial/local availability.')
    st.write('All visual previews use Bergamo, Lombardia, and Italy when planned. Only a few indicators use Lombardia and Italy only.')

if page == 'Presentation / operational schema':
    st.subheader('Operational schema')
    st.write('This page summarises the indicators selected for the dashboard, the short description to be shown in the meeting, the data source, and whether local/provincial availability is already part of the plan.')
    st.dataframe(schema_df_display, use_container_width=True, hide_index=True)
    csv = schema_df_display.to_csv(index=False).encode('utf-8')
    st.download_button('Download schema as CSV', csv, file_name='heye_dashboard_schema.csv', mime='text/csv')

    st.markdown('### Planned dashboard sections')
    st.write('After this presentation page, the menu opens the visual preview of each thematic section with placeholder data and the planned graph style.')
else:
    st.subheader(page)
    section_inds = [ind for ind in INDICATORS if ind['section'] == page]
    for ind in section_inds:
        with st.container(border=True):
            render_indicator(ind)
