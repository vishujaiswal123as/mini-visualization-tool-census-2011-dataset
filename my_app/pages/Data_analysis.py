import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')
st.sidebar.title('Interactive Analysis Page')

df = pd.read_csv('datasets/india_my_updated.csv')


pio.templates.default = "plotly"

st.set_page_config(layout='wide')
st.sidebar.title('Interactive Analysis Page')

# ————— USER INPUT: Top N —————
top_n = st.sidebar.number_input(
    "Enter Top N States to Display",
    min_value=1,
    max_value=50,
    value=7
)

# ————— LOAD DATA —————

df = df.sort_values(by='Population', ascending=False)
stateg = df.groupby('State name')

pop_state = stateg['Population'].sum().sort_values(ascending=False).head(top_n)

rural = stateg['Rural_Households'].sum().sort_values(
    ascending=False).reset_index().head(top_n)
urban = stateg['Urban_Households'].sum().sort_values(
    ascending=False).reset_index().head(top_n)

male_lit = stateg['Male_Literate'].sum().reset_index().head(top_n)
female_lit = stateg['Female_Literate'].sum().reset_index().head(top_n)

internet = stateg['Households_with_Internet'].sum().reset_index().head(top_n)
computer = stateg['Households_with_Computer'].sum().reset_index().head(top_n)

religions = df[['Hindus', 'Muslims', 'Christians', 'Sikhs',
                'Buddhists', 'Jains', 'Others_Religions']].sum().reset_index()
religions.columns = ['Religion', 'Count']

# ————— CREATE PLOTS —————
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=[
        f"Top {top_n} States by Total Population",
        f"Rural vs Urban Households (Top {top_n})",
        f"Male vs Female Literacy (Top {top_n})",
        f"Households: Internet vs Computer (Top {top_n})",
        "Religion Population Distribution"
    ],
    specs=[
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "bar", "colspan": 2}, None]
    ]
)

# ——— 1) STATE POPULATION ———
fig.add_trace(
    go.Bar(x=pop_state.index, y=pop_state.values, name="Population"),
    row=1, col=1
)

# ——— 2) RURAL VS URBAN ———
fig.add_trace(go.Bar(
    x=rural['State name'], y=rural['Rural_Households'], name="Rural"
), row=1, col=2)

fig.add_trace(go.Bar(
    x=urban['State name'], y=urban['Urban_Households'], name="Urban"
), row=1, col=2)

# ——— 3) LITERACY ———
fig.add_trace(go.Bar(
    x=male_lit['State name'], y=male_lit['Male_Literate'], name="Male Literate"
), row=2, col=1)

fig.add_trace(go.Bar(
    x=female_lit['State name'], y=female_lit['Female_Literate'], name="Female Literate"
), row=2, col=1)

# ——— 4) INTERNET VS COMPUTER ———
fig.add_trace(go.Bar(
    x=internet['State name'], y=internet['Households_with_Internet'], name="Internet"
), row=2, col=2)

fig.add_trace(go.Bar(
    x=computer['State name'], y=computer['Households_with_Computer'], name="Computer"
), row=2, col=2)

# ——— 5) RELIGION DISTRIBUTION ———
fig.add_trace(
    go.Bar(x=religions['Religion'], y=religions['Count'], name="Religion"),
    row=3, col=1
)

# ——— LAYOUT & AXES ———
fig.update_layout(
    height=1400,
    width=1100,
    title_text="📊 Demographic and Household Dashboard (2011)",
    showlegend=True,
    legend_title="Categories",
    barmode='group'
)

fig.update_xaxes(tickangle=45)
fig.update_yaxes(title_text="Count")

# ——— SHOW ———
st.plotly_chart(fig, use_container_width=True)
