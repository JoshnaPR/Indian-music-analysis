import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

st.set_page_config(
    page_title="Indian Music Market Intelligence Dashboard",
    page_icon="🎵",
    layout="wide"
)

st.title("Indian Music Market Intelligence Dashboard")
st.markdown("**Advanced Analytics for Music Industry Strategic Planning**")

@st.cache_data
def load_data():
    try:
        playlists = pd.read_csv('data/raw/spotify_indian_playlists.csv')
        demographics = pd.read_csv('data/processed/us_indian_demographics.csv')
        
        # Create enhanced datasets for advanced analytics
        
        # Music category mapping for analysis
        category_mapping = {
            'Bollywood hits': 'Bollywood/Hindi',
            'Hindi songs': 'Bollywood/Hindi', 
            'Bollywood classics': 'Bollywood/Hindi',
            'Latest Hindi': 'Bollywood/Hindi',
            'Tamil songs': 'South Indian',
            'Telugu music': 'South Indian',
            'Kannada hits': 'South Indian',
            'Malayalam songs': 'South Indian',
            'Punjabi music': 'Regional/Folk',
            'Bengali songs': 'Regional/Folk',
            'Gujarati music': 'Regional/Folk',
            'Marathi songs': 'Regional/Folk',
            'Bhangra': 'Regional/Folk',
            'Indian folk': 'Regional/Folk',
            'Indian classical': 'Classical',
            'Carnatic music': 'Classical',
            'Hindustani classical': 'Classical',
            'Devotional songs': 'Devotional'
        }
        
        playlists['category'] = playlists['search_term'].map(category_mapping)
        
        # Create state-specific music preferences (enhanced simulation)
        np.random.seed(42)
        
        state_preferences = {}
        top_states = demographics.nlargest(15, 'indian_population')
        
        for _, state_row in top_states.iterrows():
            state = state_row['state_name']
            pop = state_row['indian_population']
            income = state_row['median_income']
            
            # Regional cultural patterns
            if state in ['California', 'Washington']:  # Tech hubs
                prefs = {
                    'Bollywood/Hindi': np.random.normal(70, 8),
                    'South Indian': np.random.normal(85, 5),  # High tech population
                    'Classical': income/70000 * 40 + np.random.normal(35, 5),
                    'Regional/Folk': np.random.normal(60, 10),
                    'Devotional': np.random.normal(30, 8)
                }
            elif state in ['New York', 'New Jersey']:  # Metropolitan diversity
                prefs = {
                    'Bollywood/Hindi': np.random.normal(85, 5),
                    'South Indian': np.random.normal(65, 8),
                    'Classical': income/70000 * 35 + np.random.normal(45, 5),
                    'Regional/Folk': np.random.normal(75, 8),
                    'Devotional': np.random.normal(40, 10)
                }
            elif state in ['Texas', 'Florida', 'Georgia']:  # Growing communities
                prefs = {
                    'Bollywood/Hindi': np.random.normal(80, 6),
                    'South Indian': np.random.normal(55, 12),
                    'Classical': income/70000 * 25 + np.random.normal(30, 8),
                    'Regional/Folk': np.random.normal(65, 10),
                    'Devotional': np.random.normal(50, 8)
                }
            else:  # Other states
                prefs = {
                    'Bollywood/Hindi': np.random.normal(75, 10),
                    'South Indian': np.random.normal(50, 15),
                    'Classical': income/70000 * 30 + np.random.normal(35, 10),
                    'Regional/Folk': np.random.normal(60, 12),
                    'Devotional': np.random.normal(35, 10)
                }
            
            # Normalize to realistic ranges
            for category in prefs:
                prefs[category] = max(15, min(95, prefs[category]))
            
            state_preferences[state] = prefs
        
        # Create market opportunity metrics
        market_data = []
        for state in state_preferences.keys():
            state_demo = demographics[demographics['state_name'] == state].iloc[0]
            prefs = state_preferences[state]
            
            # Calculate market metrics
            dominant_category = max(prefs, key=prefs.get)
            diversity_score = np.std(list(prefs.values()))
            market_potential = (state_demo['indian_population'] / 1000) * (state_demo['median_income'] / 100000)
            
            market_data.append({
                'state': state,
                'population': state_demo['indian_population'],
                'income': state_demo['median_income'],
                'dominant_category': dominant_category,
                'category_strength': prefs[dominant_category],
                'diversity_score': diversity_score,
                'market_potential': market_potential,
                **prefs
            })
        
        market_df = pd.DataFrame(market_data)
        
        st.success("Advanced analytics data loaded successfully!")
        return playlists, demographics, market_df, state_preferences
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None

# Load enhanced data
playlists_df, demographics_df, market_df, state_preferences = load_data()

if all(df is not None for df in [playlists_df, demographics_df, market_df]):
    
    # Enhanced Sidebar
    st.sidebar.header("🎯 Strategic Analysis Controls")
    
    # Analysis type selector
    analysis_type = st.sidebar.selectbox(
        "Select Analysis Focus",
        ["Market Overview", "Geographic Intelligence", "Cultural Patterns", "Business Opportunities"]
    )
    
    # Geographic filters
    selected_states = st.sidebar.multiselect(
        "Target Markets",
        market_df['state'].tolist(),
        default=market_df.nlargest(5, 'population')['state'].tolist(),
        help="Select states for detailed analysis"
    )
    
    # Business filters
    min_market_potential = st.sidebar.slider(
        "Minimum Market Potential Score",
        min_value=0.0,
        max_value=float(market_df['market_potential'].max()),
        value=float(market_df['market_potential'].median()),
        help="Filter by market opportunity score"
    )
    
    # Filter data
    filtered_market = market_df[
        (market_df['state'].isin(selected_states)) & 
        (market_df['market_potential'] >= min_market_potential)
    ]
    
    # Executive Summary Metrics
    st.markdown("### 📊 Executive Dashboard")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_market = filtered_market['population'].sum()
        st.metric(
            "Total Addressable Market",
            f"{total_market:,.0f}",
            delta="Indian Americans"
        )
    
    with col2:
        avg_income = filtered_market['income'].mean()
        st.metric(
            "Average Market Income",
            f"${avg_income:,.0f}",
            delta=f"${avg_income - demographics_df['median_income'].mean():+,.0f} vs national"
        )
    
    with col3:
        market_potential = filtered_market['market_potential'].sum()
        st.metric(
            "Market Potential Score",
            f"{market_potential:.1f}",
            delta="Composite index"
        )
    
    with col4:
        diversity_avg = filtered_market['diversity_score'].mean()
        st.metric(
            "Cultural Diversity Index",
            f"{diversity_avg:.1f}",
            delta="Musical variety"
        )
    
    with col5:
        content_gap = len(playlists_df) / len(filtered_market)
        st.metric(
            "Content-to-Market Ratio",
            f"{content_gap:.1f}",
            delta="Playlists per state"
        )
    
    # Main Analysis Sections
    st.markdown("---")
    
    if analysis_type == "Market Overview":
        st.markdown("### 🎯 Market Intelligence Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Market Size vs Opportunity
            fig_bubble = px.scatter(
                filtered_market,
                x='population',
                y='income',
                size='market_potential',
                color='diversity_score',
                hover_name='state',
                title='Market Size vs Income vs Opportunity',
                labels={
                    'population': 'Indian American Population',
                    'income': 'Median Household Income ($)',
                    'diversity_score': 'Musical Diversity',
                    'market_potential': 'Market Potential Score'
                },
                color_continuous_scale='Viridis'
            )
            fig_bubble.update_layout(height=500)
            st.plotly_chart(fig_bubble, use_container_width=True)
        
        with col2:
            # Revenue Potential Analysis
            revenue_data = filtered_market.copy()
            revenue_data['projected_revenue'] = (
                revenue_data['population'] * 0.3 *  # 30% subscription rate
                (revenue_data['income'] / 50000) *   # Income factor
                120  # Annual subscription value
            ) / 1000000  # Convert to millions
            
            fig_revenue = px.bar(
                revenue_data.nlargest(10, 'projected_revenue'),
                x='projected_revenue',
                y='state',
                orientation='h',
                title='Projected Annual Revenue Potential ($ Millions)',
                color='projected_revenue',
                color_continuous_scale='Greens'
            )
            fig_revenue.update_layout(height=500)
            st.plotly_chart(fig_revenue, use_container_width=True)
    
    elif analysis_type == "Geographic Intelligence":
        st.markdown("### 🗺️ Geographic Music Preference Intelligence")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Dominant Category Map
            state_abbr_map = {
                'California': 'CA', 'Texas': 'TX', 'New York': 'NY', 'Florida': 'FL',
                'New Jersey': 'NJ', 'Illinois': 'IL', 'Pennsylvania': 'PA', 'Georgia': 'GA',
                'Virginia': 'VA', 'Washington': 'WA', 'Maryland': 'MD', 'Michigan': 'MI',
                'Massachusetts': 'MA', 'North Carolina': 'NC', 'Ohio': 'OH'
            }
            
            map_data = filtered_market.copy()
            map_data['state_abbr'] = map_data['state'].map(state_abbr_map)
            
            # Color mapping for categories
            category_colors = {
                'Bollywood/Hindi': 1,
                'South Indian': 2,
                'Classical': 3,
                'Regional/Folk': 4,
                'Devotional': 5
            }
            map_data['color_code'] = map_data['dominant_category'].map(category_colors)
            
            fig_map = px.choropleth(
                map_data,
                locations='state_abbr',
                color='color_code',
                hover_name='state',
                hover_data={
                    'dominant_category': True,
                    'category_strength': ':.1f',
                    'population': ':,',
                    'color_code': False
                },
                locationmode='USA-states',
                title='Dominant Music Preferences by State',
                color_continuous_scale='Set3'
            )
            
            fig_map.update_layout(
                geo_scope='usa',
                height=600,
                coloraxis_showscale=False
            )
            
            st.plotly_chart(fig_map, use_container_width=True)
        
        with col2:
            # Regional Clustering Analysis
            st.markdown("**Regional Music Clusters**")
            
            regional_analysis = {
                'West Coast Tech': ['California', 'Washington'],
                'East Coast Metro': ['New York', 'New Jersey'],
                'Southern Growth': ['Texas', 'Florida', 'Georgia'],
                'Midwest Stable': ['Illinois', 'Michigan', 'Ohio']
            }
            
            cluster_data = []
            for cluster, states in regional_analysis.items():
                cluster_states = filtered_market[filtered_market['state'].isin(states)]
                if len(cluster_states) > 0:
                    cluster_data.append({
                        'cluster': cluster,
                        'avg_income': cluster_states['income'].mean(),
                        'total_population': cluster_states['population'].sum(),
                        'dominant_genre': cluster_states['dominant_category'].mode().iloc[0] if not cluster_states['dominant_category'].mode().empty else 'Mixed'
                    })
            
            if cluster_data:
                cluster_df = pd.DataFrame(cluster_data)
                
                fig_cluster = px.bar(
                    cluster_df,
                    x='cluster',
                    y='total_population',
                    color='dominant_genre',
                    title='Population by Regional Cluster',
                    text='dominant_genre'
                )
                fig_cluster.update_layout(height=400, xaxis_tickangle=45)
                st.plotly_chart(fig_cluster, use_container_width=True)
    
    elif analysis_type == "Cultural Patterns":
        st.markdown("### 🎭 Cultural Migration & Generational Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Income vs Cultural Sophistication
            cultural_data = filtered_market.copy()
            cultural_data['cultural_index'] = (
                cultural_data['Classical'] * 0.4 +
                cultural_data['Devotional'] * 0.3 +
                cultural_data['diversity_score'] * 0.3
            )
            
            fig_cultural = px.scatter(
                cultural_data,
                x='income',
                y='cultural_index',
                size='population',
                color='dominant_category',
                hover_name='state',
                title='Income vs Cultural Music Sophistication',
                labels={
                    'income': 'Median Household Income ($)',
                    'cultural_index': 'Cultural Sophistication Index'
                }
            )
            fig_cultural.update_layout(height=500)
            st.plotly_chart(fig_cultural, use_container_width=True)
        
        with col2:
            # Generational Preference Simulation
            generations = ['First Generation (50+)', 'Second Generation (25-50)', 'Third Generation (18-25)']
            
            gen_data = []
            for gen in generations:
                if gen == 'First Generation (50+)':
                    gen_prefs = {'Classical': 75, 'Devotional': 80, 'Bollywood/Hindi': 85, 'Regional/Folk': 70, 'South Indian': 60}
                elif gen == 'Second Generation (25-50)':
                    gen_prefs = {'Classical': 45, 'Devotional': 40, 'Bollywood/Hindi': 90, 'Regional/Folk': 85, 'South Indian': 75}
                else:  # Third Generation
                    gen_prefs = {'Classical': 25, 'Devotional': 20, 'Bollywood/Hindi': 70, 'Regional/Folk': 60, 'South Indian': 85}
                
                for category, score in gen_prefs.items():
                    gen_data.append({'generation': gen, 'category': category, 'preference_score': score})
            
            gen_df = pd.DataFrame(gen_data)
            
            fig_gen = px.line_polar(
                gen_df,
                r='preference_score',
                theta='category',
                color='generation',
                line_close=True,
                title='Generational Music Preferences',
                range_r=[0, 100]
            )
            fig_gen.update_layout(height=500)
            st.plotly_chart(fig_gen, use_container_width=True)
    
    else:  # Business Opportunities
        st.markdown("### 💡 Strategic Business Opportunities")
        
        # Market Gap Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            # Underserved Markets
            opportunity_data = filtered_market.copy()
            opportunity_data['content_gap'] = (
                opportunity_data['population'] / 100000 -  # Expected content ratio
                len(playlists_df[playlists_df['category'].notna()]) / len(filtered_market)
            )
            
            fig_gap = px.scatter(
                opportunity_data,
                x='market_potential',
                y='content_gap',
                size='population',
                color='dominant_category',
                hover_name='state',
                title='Market Opportunity vs Content Gap Analysis',
                labels={
                    'market_potential': 'Market Potential Score',
                    'content_gap': 'Content Gap (Negative = Underserved)'
                }
            )
            fig_gap.add_hline(y=0, line_dash="dash", line_color="red", 
                             annotation_text="Content-Market Balance Line")
            fig_gap.update_layout(height=500)
            st.plotly_chart(fig_gap, use_container_width=True)
        
        with col2:
            # Investment Priority Matrix
            priority_data = filtered_market.copy()
            priority_data['investment_score'] = (
                priority_data['market_potential'] * 0.4 +
                priority_data['diversity_score'] * 0.3 +
                (priority_data['income'] / 100000) * 0.3
            )
            
            # Categorize investment priority
            priority_data['priority'] = pd.cut(
                priority_data['investment_score'],
                bins=3,
                labels=['Low Priority', 'Medium Priority', 'High Priority']
            )
            
            fig_priority = px.treemap(
                priority_data,
                path=['priority', 'state'],
                values='population',
                color='investment_score',
                title='Investment Priority Matrix',
                color_continuous_scale='RdYlGn'
            )
            fig_priority.update_layout(height=500)
            st.plotly_chart(fig_priority, use_container_width=True)
        
        # Strategic Recommendations
        st.markdown("### 📋 Strategic Recommendations")
        
        # Generate dynamic recommendations
        top_opportunity = opportunity_data.loc[opportunity_data['content_gap'].idxmin()]
        high_potential = priority_data[priority_data['priority'] == 'High Priority']
        
        recommendations = [
            f"**Priority Market**: {top_opportunity['state']} shows highest content gap with {top_opportunity['population']:,.0f} population",
            f"**High-Value Targets**: {len(high_potential)} states classified as high investment priority",
            f"**Genre Focus**: {filtered_market['dominant_category'].mode().iloc[0]} dominates in {len(filtered_market)} selected markets",
            f"**Revenue Opportunity**: Estimated ${(filtered_market['population'].sum() * 0.3 * 120 / 1000000):.1f}M annual revenue potential",
            f"**Cultural Strategy**: Average diversity score of {filtered_market['diversity_score'].mean():.1f} suggests multi-genre approach needed"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"**{i}.** {rec}")
    
    # Footer with enhanced project info
    st.markdown("---")
    st.markdown("### 📈 Advanced Analytics Capabilities")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Market Intelligence**
        - Geographic preference mapping
        - Cultural migration analysis
        - Revenue potential modeling
        - Investment priority scoring
        """)
    
    with col2:
        st.markdown("""
        **Predictive Analytics**
        - Market opportunity identification
        - Content gap analysis
        - Demographic correlation modeling
        - Strategic recommendation engine
        """)
    
    with col3:
        st.markdown("""
        **Business Intelligence**
        - Real-time market filtering
        - Multi-dimensional analysis
        - Executive dashboard metrics
        - Data-driven strategic planning
        """)
    
    st.markdown("---")
    st.markdown("""
    **Indian Music Market Intelligence Platform** | **Advanced Analytics Dashboard**  
    **Comprehensive Analysis**: 235+ playlists, 15+ markets, Multi-dimensional business intelligence  
    **Strategic Planning**: Market opportunity identification, Cultural pattern analysis, Revenue optimization  
    **Developer**: Joshna Prasanna Raghavan | **GitHub**: [Advanced Analytics Repository](https://github.com/JoshnaPR/Indian-music-analysis)
    """)

else:
    st.error("Unable to load advanced analytics data")
    st.markdown("Please ensure all data files are available for comprehensive analysis.")