import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd


st.set_page_config(layout='wide')
st.title("India Census 2011 Data Visualization")

df = pd.read_csv('datasets/india_census2011_project.csv')

geojson_path = 'datasets/india.geojson'
gdf = gpd.read_file(geojson_path)
gdf['district'] = gdf['district'].str.strip().str.upper()

list_of_states = list(df['State name'].unique())
list_of_states.sort()
list_of_states.insert(0,'Overall India')

st.sidebar.title('Home Page')

selected_state = st.sidebar.selectbox('Select a state or a Union Teritory',list_of_states)
primary = st.sidebar.selectbox('Select Primary Parameter',sorted(df.columns[:]))
secondary = st.sidebar.multiselect('Select Secondary Parameter',sorted(df.columns[:]))

color_scale=['Viridis','Blues','Greens','Reds','Oranges','Purples','Greys','YlGn','YlGnBu','YlOrBr','YlOrRd','PuBu','PuBuGn','BuGn','BuPu','RdPu','PuRd','GnBu','OrRd','Cividis','Plasma','Inferno','Magma','Turbo','Blackbody','Hot','Electric']

selected_scale= st.sidebar.selectbox('Select color scale',color_scale)

order = [
    'State name', 'District name', 'District code', 'Population', 'Male',
    'Female', 'Literate', 'Male_Literate', 'Female_Literate', 
    'Male_percentage', 'Female_percentage', 'Male_literacy_percent',
    'Female_literacy_percent', 'Sex_ratio',
    'Hindus', 'Muslims', 'Christians',
    'Sikhs', 'Buddhists', 'Jains', 'Others_Religions',
    'Households', 'Rural_Households', 'Urban_Households',
    'Housholds_with_Electric_Lighting', 'LPG_or_PNG_Households',
    'Households_with_Internet', 'Households_with_Computer',
    'Households_with_Television', 'Households_with_Telephone_Mobile_Phone',
    'Households_with_Car_Jeep_Van'
]

day_order = {col: i for i, col in enumerate(order)}
secondary = sorted(secondary, key=lambda x: day_order.get(x, 999))



plot = st.sidebar.button('Plot Graph')

if plot:

  st.text('Color represents primary parameter')
  st.text('Secodary parameter add columns (more Info) which you want when you hover over the map add more detailes')
  if len(secondary) > 24:
    st.warning("Please select at most 24 secondary parameters to avoid cluttering the hover information.")
  else:    
    if selected_state == 'Overall India':
        # plot for india
        fig =  fig = px.choropleth_map(df,
        geojson=gdf.__geo_interface__,
        locations='District name',
        featureidkey="properties.district",
        color=primary,   # choose any column
        color_continuous_scale=selected_scale,
        map_style="carto-positron",
        zoom=4,
        center={"lat": 22.9734, "lon": 78.6569},
        opacity=0.6
        ,hover_name='District name'
        ,hover_data=secondary
         )
        st.plotly_chart(fig,use_container_width=True)
        
    else:
        # plot for state
        state_df = df[df['State name'] == selected_state]

        fig = fig = px.choropleth_map(
        state_df,
        geojson=gdf.__geo_interface__,
        locations='District name',
        featureidkey="properties.district",
        color=primary,                # choose any column
        color_continuous_scale=selected_scale,
        map_style="carto-positron",
        zoom=4,
        center={"lat": 22.9734, "lon": 78.6569},
        opacity=0.6
        ,hover_name='District name'
        ,hover_data=secondary
      )
        st.plotly_chart(fig, use_container_width=True)



