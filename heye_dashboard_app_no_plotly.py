import streamlit as st
import pandas as pd

st.set_page_config(page_title='HEYE Dashboard', layout='wide')

st.title('HEYE Dashboard')
st.caption('Prototype: Bergamo vs Lombardia vs Italia')

# Demo data
territories = ['Bergamo', 'Lombardia', 'Italia']
years = [2018, 2019, 2020, 2021, 2022, 2023]

rows = []
for terr, occ, neet, tertiary, netmig, income, wellbeing in [
    ('Bergamo', [69,70,68,69,71,72], [14,13,15,16,14,13], [29,30,31,31,32,33], [2.5,2.4,1.2,0.8,1.5,1.9], [22000,22500,22100,22800,23300,23800], [6.8,6.7,6.3,6.4,6.6,6.7]),
    ('Lombardia', [67,68,66,67,69,70], [16,15,17,18,16,15], [27,28,29,29,30,31], [1.4,1.2,0.5,0.2,0.8,1.0], [21000,21400,21000,21600,22100,22600], [6.6,6.5,6.1,6.2,6.4,6.5]),
    ('Italia', [58,59,57,58,60,61], [23,22,24,25,23,22], [20,21,22,22,23,24], [-0.6,-0.8,-1.0,-1.1,-0.7,-0.5], [18000,18300,17900,18400,18800,19200], [6.1,6.0,5.8,5.8,5.9,6.0]),
]:
    for i, y in enumerate(years):
        rows.append({
            'territory': terr,
            'year': y,
            'employment_rate': occ[i],
            'neet_rate': neet[i],
            'tertiary_share': tertiary[i],
            'net_migration_20_39': netmig[i],
            'equiv_income': income[i],
            'wellbeing': wellbeing[i],
        })

df = pd.DataFrame(rows)

page = st.sidebar.radio('Section', [
    'Overview',
    'Population & Education',
    'Employment & Job Quality',
    'Mobility & Retention',
    'Economic Autonomy',
    'Well-being & Perceptions',
    'Data Notes'
])

latest = df[df['year'] == df['year'].max()].set_index('territory')

if page == 'Overview':
    c1, c2, c3, c4 = st.columns(4)
    c1.metric('Employment rate 2023 (Bergamo)', f"{latest.loc['Bergamo','employment_rate']}%")
    c2.metric('NEET rate 2023 (Bergamo)', f"{latest.loc['Bergamo','neet_rate']}%")
    c3.metric('Tertiary share 2023 (Bergamo)', f"{latest.loc['Bergamo','tertiary_share']}%")
    c4.metric('Net migration 20-39 2023 (Bergamo)', f"{latest.loc['Bergamo','net_migration_20_39']}")

    st.subheader('Employment trend')
    pivot = df.pivot(index='year', columns='territory', values='employment_rate')
    st.line_chart(pivot)

    st.subheader('NEET trend')
    pivot = df.pivot(index='year', columns='territory', values='neet_rate')
    st.line_chart(pivot)

elif page == 'Population & Education':
    st.subheader('Tertiary education share')
    pivot = df.pivot(index='year', columns='territory', values='tertiary_share')
    st.line_chart(pivot)
    st.write('Use this page for youth cohort size, tertiary enrolment, completion, and pipeline indicators once real data are added.')

elif page == 'Employment & Job Quality':
    st.subheader('Employment rate')
    st.line_chart(df.pivot(index='year', columns='territory', values='employment_rate'))
    st.subheader('NEET rate')
    st.line_chart(df.pivot(index='year', columns='territory', values='neet_rate'))
    st.write('Add temporary contracts, involuntary part-time, and job quality proxies here.')

elif page == 'Mobility & Retention':
    st.subheader('Net migration age 20-39')
    st.line_chart(df.pivot(index='year', columns='territory', values='net_migration_20_39'))
    st.write('Better to replace this later with inflow, outflow, and retention indicators, not net balance only.')

elif page == 'Economic Autonomy':
    st.subheader('Equivalent income')
    st.line_chart(df.pivot(index='year', columns='territory', values='equiv_income'))
    st.write('Later add housing burden, arrears, financial vulnerability, and an autonomy/stability index.')

elif page == 'Well-being & Perceptions':
    st.subheader('Well-being')
    st.line_chart(df.pivot(index='year', columns='territory', values='wellbeing'))
    st.write('Later add perceived stability, future expectations, and social isolation indicators when data are available.')

elif page == 'Data Notes':
    st.markdown('''
**Current status**
- This is a visual prototype with placeholder values.
- Replace demo data with CSV files or direct data processing scripts.
- Keep all comparisons fixed on Bergamo, Lombardia, and Italia.

**Suggested data sources**
- Public territorial statistics for first release
- EU-SILC / SHIW for economic conditions
- ESS / CRONOS for perceptions and well-being
- Administrative or local sources for Bergamo-specific updates
''')
