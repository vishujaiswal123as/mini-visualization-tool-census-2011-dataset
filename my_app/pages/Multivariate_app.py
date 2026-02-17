import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')
st.sidebar.title('Multivariate Analysis Page')


df = pd.read_csv('india_my_updated.csv')

list_of_states = list(df['State name'].unique())
list_of_states.insert(0,'Overall India')


selected_state = st.sidebar.selectbox('Select a state',list_of_states)
primary = st.sidebar.selectbox('Select Primary Parameter',sorted(df.columns[5:]))
secondary = st.sidebar.selectbox('Select Secondary Parameter',sorted(df.columns[5:]))

plot = st.sidebar.button('Plot Graph')

if plot:

    st.text('Size represent primary parameter')
    st.text('Color represents secondary parameter')
    if selected_state == 'Overall India':
        # plot for india
        fig = px.scatter_mapbox(df, lat="lat", lon="lon", size=primary, color=secondary, zoom=4,size_max=35,
                                mapbox_style="carto-positron",width=1200,height=700,hover_name='district')

        st.plotly_chart(fig,use_container_width=True)
    else:
        # plot for state
        state_df = df[df['State name'] == selected_state]

        fig = px.scatter_mapbox(state_df, lat="lat", lon="lon", size=primary, color=secondary, zoom=6, size_max=35,
                                mapbox_style="carto-positron", width=1100, height=700,hover_name='district')

        st.plotly_chart(fig, use_container_width=True)



