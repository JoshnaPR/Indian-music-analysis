import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Indian Music Analysis Dashboard",
    layout="wide"
)

st.title("Indian Music Listeners in the US Dashboard")
st.markdown("Interactive Analysis of Indian Music Preferences Across US Demographics")

@st.cache_data
def load_data():
    try:
        playlists = pd.read_csv('data/raw/spotify_indian_playlists.csv')
        demographics = pd.read_csv('data/processed/us_indian_demographics.csv')
        st.success("Data loaded successfully!")
        return playlists, demographics
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.write("Current directory:", os.getcwd())
        st.write("Files:", os.listdir('.'))
        if os.path.exists('data'):
            st.write("Data folder contents:", os.listdir('data'))
        return None, None

playlists_df, demographics_df = load_data()

if playlists_df is not None and demographics_df is not None:
    
    st.sidebar.header("Filters")
    
    selected_states = st.sidebar.multiselect(
        "Select States",
        demographics_df['state_name'].tolist(),
        default=demographics_df.nlargest(5, 'indian_population')['state_name'].tolist()
    )
    
    filtered_demographics = demographics_df[demographics_df['state_name'].isin(selected_states)]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("States", len(filtered_demographics))
    
    with col2:
        st.metric("Playlists", len(playlists_df))
    
    with col3:
        st.metric("Population", f"{filtered_demographics['indian_population'].sum():,}")
    
    st.subheader("Population by State")
    
    fig_bar = px.bar(
        filtered_demographics.nlargest(10, 'indian_population'),
        x='indian_population',
        y='state_name',
        orientation='h',
        title='Top States by Indian Population'
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.subheader("Music Categories")
    
    category_counts = playlists_df['search_term'].value_counts()
    
    fig_pie = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        title='Music Category Distribution'
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.subheader("Data Tables")
    
    tab1, tab2 = st.tabs(["Demographics", "Playlists"])
    
    with tab1:
        st.dataframe(filtered_demographics)
    
    with tab2:
        st.dataframe(playlists_df)

else:
    st.error("Could not load data files")