import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add parent directory to path to import data
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Configure the page
st.set_page_config(
    page_title="Indian Music Analysis Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Title and header
st.markdown('<h1 class="main-header">Indian Music Listeners in the US Dashboard</h1>', unsafe_allow_html=True)
st.markdown("### Interactive Analysis of Indian Music Preferences Across US Demographics")

# Load data with error handling
@st.cache_data
def load_data():
    try:
        # Load all the datasets we created
        playlists = pd.read_csv('../data/raw/spotify_indian_playlists.csv')
        demographics = pd.read_csv('../data/processed/us_indian_demographics.csv')
        
        # If rankings file exists, load it, otherwise create sample data
        try:
            rankings = pd.read_csv('../data/processed/state_music_rankings.csv', index_col=0)
        except:
            # Create sample rankings data if file doesn't exist
            import numpy as np
            np.random.seed(42)
            top_states = demographics.nlargest(10, 'indian_population')['state_name'].tolist()
            categories = ['Bollywood/Hindi', 'South Indian', 'Classical', 'Regional/Folk', 'Devotional']
            rankings_data = {}
            for state in top_states:
                rankings_data[state] = {cat: np.random.randint(1, 6) for cat in categories}
            rankings = pd.DataFrame(rankings_data).T
        
        return playlists, demographics, rankings
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

# Load the data
playlists_df, demographics_df, rankings_df = load_data()

if playlists_df is not None and demographics_df is not None:
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # State selection
    selected_states = st.sidebar.multiselect(
        "Select States to Analyze",
        demographics_df['state_name'].tolist(),
        default=demographics_df.nlargest(5, 'indian_population')['state_name'].tolist()
    )
    
    # Music category filter
    music_categories = ['Bollywood hits', 'Hindi songs', 'Tamil songs', 'Telugu music', 
                       'Punjabi music', 'Bengali songs', 'Indian classical', 'Devotional songs']
    selected_categories = st.sidebar.multiselect(
        "Select Music Categories",
        music_categories,
        default=music_categories[:4]
    )
    
    # Population threshold
    min_population = st.sidebar.slider(
        "Minimum Indian Population",
        min_value=0,
        max_value=int(demographics_df['indian_population'].max()),
        value=50000,
        step=10000
    )
    
    # Filter data based on selections
    filtered_demographics = demographics_df[
        (demographics_df['state_name'].isin(selected_states)) & 
        (demographics_df['indian_population'] >= min_population)
    ]
    
    filtered_playlists = playlists_df[playlists_df['search_term'].isin(selected_categories)]
    
    # Main dashboard layout
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="States Analyzed",
            value=len(filtered_demographics),
            delta=f"{len(selected_states)} selected"
        )
    
    with col2:
        st.metric(
            label="Playlists Found",
            value=len(filtered_playlists),
            delta=f"{len(selected_categories)} categories"
        )
    
    with col3:
        st.metric(
            label="Total Population",
            value=f"{filtered_demographics['indian_population'].sum():,}",
            delta="Indian Americans"
        )
    
    with col4:
        st.metric(
            label="Avg Income",
            value=f"${filtered_demographics['median_income'].mean():,.0f}",
            delta="Median household"
        )
    
    # Row 1: Maps and geographic analysis
    st.markdown("---")
    st.markdown("## Geographic Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Indian Population by State")
        
        # Create choropleth map
        fig_map = px.choropleth(
            filtered_demographics,
            locations='state_abbr' if 'state_abbr' in filtered_demographics.columns else 'state_name',
            color='indian_population',
            hover_name='state_name',
            hover_data={'indian_population': ':,', 'median_income': ':$,'},
            locationmode='USA-states',
            color_continuous_scale='Viridis',
            title='Indian American Population Distribution'
        )
        
        fig_map.update_layout(
            geo_scope='usa',
            height=400
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    
    with col2:
        st.markdown("### Top States by Population")
        
        # Bar chart of top states
        top_states = filtered_demographics.nlargest(10, 'indian_population')
        
        fig_bar = px.bar(
            top_states,
            x='indian_population',
            y='state_name',
            orientation='h',
            title='Top 10 States by Indian Population',
            color='indian_population',
            color_continuous_scale='Blues'
        )
        
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Row 2: Music analysis
    st.markdown("---")
    st.markdown("## Music Preferences Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Music Category Distribution")
        
        # Pie chart of music categories
        category_counts = filtered_playlists['search_term'].value_counts()
        
        fig_pie = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title='Distribution of Playlists by Category'
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("### Income vs Population Analysis")
        
        # Scatter plot
        fig_scatter = px.scatter(
            filtered_demographics,
            x='indian_population',
            y='median_income',
            size='indian_population',
            hover_name='state_name',
            title='Income vs Population by State',
            color='median_income',
            color_continuous_scale='Viridis'
        )
        
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Row 3: Rankings and detailed analysis
    if rankings_df is not None and len(rankings_df) > 0:
        st.markdown("---")
        st.markdown("## State Music Preference Rankings")
        
        # Filter rankings for selected states
        available_states = [state for state in selected_states if state in rankings_df.index]
        
        if available_states:
            filtered_rankings = rankings_df.loc[available_states]
            
            # Heatmap of rankings
            fig_heatmap = px.imshow(
                filtered_rankings.values,
                x=filtered_rankings.columns,
                y=filtered_rankings.index,
                color_continuous_scale='RdYlBu_r',
                title='Music Category Rankings by State (1=Most Popular, 5=Least Popular)',
                text_auto=True
            )
            
            fig_heatmap.update_layout(height=500)
            st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Row 4: Data tables and insights
    st.markdown("---")
    st.markdown("## Detailed Data Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Demographics", "Playlists", "Insights"])
    
    with tab1:
        st.markdown("### State Demographics Data")
        st.dataframe(
            filtered_demographics[['state_name', 'indian_population', 'median_income', 'median_rent']],
            use_container_width=True
        )
    
    with tab2:
        st.markdown("### Playlist Analysis")
        
        # Group playlists by category
        playlist_summary = filtered_playlists.groupby('search_term').agg({
            'playlist_name': 'count',
            'total_tracks': ['mean', 'sum'],
            'followers': 'mean'
        }).round(2)
        
        playlist_summary.columns = ['Playlist Count', 'Avg Tracks', 'Total Tracks', 'Avg Followers']
        st.dataframe(playlist_summary, use_container_width=True)
    
    with tab3:
        st.markdown("### Key Insights")
        
        # Generate dynamic insights
        top_state = filtered_demographics.loc[filtered_demographics['indian_population'].idxmax(), 'state_name']
        top_category = filtered_playlists['search_term'].value_counts().index[0]
        avg_income = filtered_demographics['median_income'].mean()
        
        insights = [
            f"**{top_state}** leads with the highest Indian American population among selected states",
            f"**{top_category}** is the most represented music category in your selection",
            f"Average household income in selected states: **${avg_income:,.0f}**",
            f"Total playlists analyzed: **{len(filtered_playlists)}** across **{len(selected_categories)}** categories",
            f"Geographic coverage: **{len(filtered_demographics)}** states with **{filtered_demographics['indian_population'].sum():,}** Indian Americans"
        ]
        
        for insight in insights:
            st.markdown(insight)
    
    # Footer
    st.markdown("---")
    st.markdown("###  About This Dashboard")
    st.markdown("""
    This interactive dashboard analyimport streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add parent directory to path to import data
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Configure the page
st.set_page_config(
    page_title="Indian Music Analysis Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Title and header
st.markdown('<h1 class="main-header">🎵 Indian Music Listeners in the US Dashboard</h1>', unsafe_allow_html=True)
st.markdown("### Interactive Analysis of Indian Music Preferences Across US Demographics")

# Load data with error handling
@st.cache_data
def load_data():
    try:
        # Try different path strategies for deployment vs local
        data_paths = [
            # For Streamlit deployment
            ('data/raw/spotify_indian_playlists.csv', 'data/processed/us_indian_demographics.csv'),
            # For local development  
            ('../data/raw/spotify_indian_playlists.csv', '../data/processed/us_indian_demographics.csv'),
            # Alternative paths
            ('./data/raw/spotify_indian_playlists.csv', './data/processed/us_indian_demographics.csv')
        ]
        
        playlists = None
        demographics = None
        
        for playlist_path, demo_path in data_paths:
            try:
                playlists = pd.read_csv(playlist_path)
                demographics = pd.read_csv(demo_path)
                st.success(f"✅ Data loaded successfully from {playlist_path}")
                break
            except FileNotFoundError:
                continue
        
        if playlists is None or demographics is None:
            raise FileNotFoundError("Could not find data files in any expected location")
        
        # Handle rankings data
        try:
            rankings_paths = [
                'data/processed/state_music_rankings.csv',
                '../data/processed/state_music_rankings.csv',
                './data/processed/state_music_rankings.csv'
            ]
            rankings = None
            for path in rankings_paths:
                try:
                    rankings = pd.read_csv(path, index_col=0)
                    break
                except FileNotFoundError:
                    continue
                    
            if rankings is None:
                # Create sample rankings data if file doesn't exist
                import numpy as np
                np.random.seed(42)
                top_states = demographics.nlargest(10, 'indian_population')['state_name'].tolist()
                categories = ['Bollywood/Hindi', 'South Indian', 'Classical', 'Regional/Folk', 'Devotional']
                rankings_data = {}
                for state in top_states:
                    rankings_data[state] = {cat: np.random.randint(1, 6) for cat in categories}
                rankings = pd.DataFrame(rankings_data).T
                st.info("📊 Using sample rankings data (original file not found)")
        except Exception as e:
            st.warning(f"Note: Rankings data not available ({e})")
            rankings = None
        
        return playlists, demographics, rankings
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        
        # Show debug information
        import os
        st.write("**Debug: Current working directory:**", os.getcwd())
        st.write("**Debug: Files in current directory:**")
        try:
            files = os.listdir('.')
            st.write(files)
        except:
            st.write("Could not list files")
            
        st.write("**Debug: Looking for data directory:**")
        try:
            if os.path.exists('data'):
                st.write("✅ 'data' directory found")
                st.write("Contents:", os.listdir('data'))
                if os.path.exists('data/raw'):
                    st.write("✅ 'data/raw' found, contents:", os.listdir('data/raw'))
                if os.path.exists('data/processed'):
                    st.write("✅ 'data/processed' found, contents:", os.listdir('data/processed'))
            else:
                st.write("❌ 'data' directory not found")
        except Exception as debug_e:
            st.write(f"Debug error: {debug_e}")
            
        return None, None, None

# Load the data
playlists_df, demographics_df, rankings_df = load_data()

if playlists_df is not None and demographics_df is not None:
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # State selection
    selected_states = st.sidebar.multiselect(
        "Select States to Analyze",
        demographics_df['state_name'].tolist(),
        default=demographics_df.nlargest(5, 'indian_population')['state_name'].tolist()
    )
    
    # Music category filter
    music_categories = ['Bollywood hits', 'Hindi songs', 'Tamil songs', 'Telugu music', 
                       'Punjabi music', 'Bengali songs', 'Indian classical', 'Devotional songs']
    selected_categories = st.sidebar.multiselect(
        "Select Music Categories",
        music_categories,
        default=music_categories[:4]
    )
    
    # Population threshold
    min_population = st.sidebar.slider(
        "Minimum Indian Population",
        min_value=0,
        max_value=int(demographics_df['indian_population'].max()),
        value=50000,
        step=10000
    )
    
    # Filter data based on selections
    filtered_demographics = demographics_df[
        (demographics_df['state_name'].isin(selected_states)) & 
        (demographics_df['indian_population'] >= min_population)
    ]
    
    filtered_playlists = playlists_df[playlists_df['search_term'].isin(selected_categories)]
    
    # Main dashboard layout
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🏠 States Analyzed",
            value=len(filtered_demographics),
            delta=f"{len(selected_states)} selected"
        )
    
    with col2:
        st.metric(
            label="🎵 Playlists Found",
            value=len(filtered_playlists),
            delta=f"{len(selected_categories)} categories"
        )
    
    with col3:
        st.metric(
            label="👥 Total Population",
            value=f"{filtered_demographics['indian_population'].sum():,}",
            delta="Indian Americans"
        )
    
    with col4:
        st.metric(
            label="💰 Avg Income",
            value=f"${filtered_demographics['median_income'].mean():,.0f}",
            delta="Median household"
        )
    
    # Row 1: Maps and geographic analysis
    st.markdown("---")
    st.markdown("## 🗺️ Geographic Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Indian Population by State")
        
        # Create choropleth map
        # Handle both state_abbr and state_code columns
        location_col = 'state_abbr' if 'state_abbr' in filtered_demographics.columns else 'state_code'
        if location_col not in filtered_demographics.columns:
            # Create state abbreviations from state names
            state_abbr_map = {
                'California': 'CA', 'Texas': 'TX', 'New York': 'NY', 'Florida': 'FL',
                'New Jersey': 'NJ', 'Illinois': 'IL', 'Pennsylvania': 'PA', 'Georgia': 'GA',
                'Virginia': 'VA', 'Washington': 'WA', 'Maryland': 'MD', 'Michigan': 'MI',
                'Massachusetts': 'MA', 'North Carolina': 'NC', 'Ohio': 'OH'
            }
            filtered_demographics['state_abbr'] = filtered_demographics['state_name'].map(state_abbr_map)
            location_col = 'state_abbr'
        
        fig_map = px.choropleth(
            filtered_demographics,
            locations=location_col,
            color='indian_population',
            hover_name='state_name',
            hover_data={'indian_population': ':,', 'median_income': ':$,'},
            locationmode='USA-states',
            color_continuous_scale='Viridis',
            title='Indian American Population Distribution'
        )
        
        fig_map.update_layout(
            geo_scope='usa',
            height=400
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    
    with col2:
        st.markdown("### Top States by Population")
        
        # Bar chart of top states
        top_states = filtered_demographics.nlargest(10, 'indian_population')
        
        fig_bar = px.bar(
            top_states,
            x='indian_population',
            y='state_name',
            orientation='h',
            title='Top 10 States by Indian Population',
            color='indian_population',
            color_continuous_scale='Blues'
        )
        
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Row 2: Music analysis
    st.markdown("---")
    st.markdown("## 🎵 Music Preferences Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Music Category Distribution")
        
        # Pie chart of music categories
        category_counts = filtered_playlists['search_term'].value_counts()
        
        fig_pie = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title='Distribution of Playlists by Category'
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("### Income vs Population Analysis")
        
        # Scatter plot
        fig_scatter = px.scatter(
            filtered_demographics,
            x='indian_population',
            y='median_income',
            size='indian_population',
            hover_name='state_name',
            title='Income vs Population by State',
            color='median_income',
            color_continuous_scale='Viridis'
        )
        
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Row 3: Rankings and detailed analysis
    if rankings_df is not None and len(rankings_df) > 0:
        st.markdown("---")
        st.markdown("## 🏆 State Music Preference Rankings")
        
        # Filter rankings for selected states
        available_states = [state for state in selected_states if state in rankings_df.index]
        
        if available_states:
            filtered_rankings = rankings_df.loc[available_states]
            
            # Heatmap of rankings
            fig_heatmap = px.imshow(
                filtered_rankings.values,
                x=filtered_rankings.columns,
                y=filtered_rankings.index,
                color_continuous_scale='RdYlBu_r',
                title='Music Category Rankings by State (1=Most Popular, 5=Least Popular)',
                text_auto=True
            )
            
            fig_heatmap.update_layout(height=500)
            st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Row 4: Data tables and insights
    st.markdown("---")
    st.markdown("## 📊 Detailed Data Analysis")
    
    tab1, tab2, tab3 = st.tabs(["📈 Demographics", "🎵 Playlists", "💡 Insights"])
    
    with tab1:
        st.markdown("### State Demographics Data")
        st.dataframe(
            filtered_demographics[['state_name', 'indian_population', 'median_income', 'median_rent']],
            use_container_width=True
        )
    
    with tab2:
        st.markdown("### Playlist Analysis")
        
        # Group playlists by category
        playlist_summary = filtered_playlists.groupby('search_term').agg({
            'playlist_name': 'count',
            'total_tracks': ['mean', 'sum'],
            'followers': 'mean'
        }).round(2)
        
        playlist_summary.columns = ['Playlist Count', 'Avg Tracks', 'Total Tracks', 'Avg Followers']
        st.dataframe(playlist_summary, use_container_width=True)
    
    with tab3:
        st.markdown("### 💡 Key Insights")
        
        # Generate dynamic insights
        if len(filtered_demographics) > 0:
            top_state = filtered_demographics.loc[filtered_demographics['indian_population'].idxmax(), 'state_name']
            avg_income = filtered_demographics['median_income'].mean()
        else:
            top_state = "N/A"
            avg_income = 0
            
        if len(filtered_playlists) > 0:
            top_category = filtered_playlists['search_term'].value_counts().index[0]
        else:
            top_category = "N/A"
        
        insights = [
            f"🏆 **{top_state}** leads with the highest Indian American population among selected states",
            f"🎵 **{top_category}** is the most represented music category in your selection",
            f"💰 Average household income in selected states: **${avg_income:,.0f}**",
            f"📊 Total playlists analyzed: **{len(filtered_playlists)}** across **{len(selected_categories)}** categories",
            f"🗺️ Geographic coverage: **{len(filtered_demographics)}** states with **{filtered_demographics['indian_population'].sum():,}** Indian Americans"
        ]
        
        for insight in insights:
            st.markdown(insight)
    
    # Footer
    st.markdown("---")
    st.markdown("### 📝 About This Dashboard")
    st.markdown("""
    This interactive dashboard analyzes Indian music listening patterns across US demographics using:
    - **Spotify Web API** data for music preferences
    - **US Census Bureau** data for demographic analysis
    - **Interactive filtering** for customized insights
    
    **Data Sources**: 235+ playlists, 50 states, 5 music categories
    **Developer**: Joshna Prasanna Raghavan
    **GitHub**: [Project Repository](https://github.com/JoshnaPR/Indian-music-analysis)
    """)

else:
    st.error("Unable to load data. Please check that data files exist in the correct directories.")
    st.markdown("""
    **Expected file structure:**
    ```
    data/
    ├── raw/spotify_indian_playlists.csv
    └── processed/us_indian_demographics.csv
    ```
    """)zes Indian music listening patterns across US demographics using:
    - **Spotify Web API** data for music preferences
    - **US Census Bureau** data for demographic analysis
    - **Interactive filtering** for customized insights
    
    **Data Sources**: 235+ playlists, 50 states, 5 music categories
    **Developer**: Joshna Prasanna Raghavan
    **GitHub**: [Project Repository](https://github.com/JoshnaPR/Indian-music-analysis)
    """)

else:
    st.error("Unable to load data. Please check that data files exist in the correct directories.")
    st.markdown("""
    **Expected file structure:**
    ```
    data/
    ├── raw/spotify_indian_playlists.csv
    └── processed/us_indian_demographics.csv
    ```
    """)