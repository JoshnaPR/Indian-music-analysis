# Indian Music Listeners in the US - Data Analytics Project

## Project Overview

This project analyzes Indian music listening patterns among different demographic groups across the United States, combining Spotify music data with US Census demographics to uncover regional preferences and market opportunities.

**Live Demo**: https://indian-music-analysis-joshnapr.streamlit.app/  
**Portfolio Type**: Data Analytics & Geographic Analysis  
**Development Timeline**: 3 weeks  

## Key Research Questions

1. Where are Indian music listeners concentrated across US states?
2. How do music preferences vary by region and demographics?
3. Which states offer the greatest potential for music streaming platforms?
4. What is the balance between Bollywood, regional, and classical music preferences?

## Key Findings

### Market Concentration
- Top 5 states contain 67.8% of Indian American population
- California leads with highest South Indian music preference
- Texas and Florida follow as major markets with diverse musical tastes

### Musical Diversity Insights
- Regional/Folk music surprisingly dominates playlist counts (32.3%)
- Bollywood vs South Indian preferences are balanced across most states
- Classical music shows correlation with higher-income demographics

### Business Opportunities
- Premium markets: CA, NY, NJ show high income + high population
- Underserved segments: Classical and devotional music categories
- Regional targeting: West Coast favors South Indian, East Coast prefers Bollywood

## Technical Stack

### Data Sources
- Spotify Web API: 235 Indian music playlists across 18 search categories
- US Census Bureau API: Demographics for all 50 states
- Data Coverage: 15 top states by Indian population, 5 music categories

### Technologies Used
- Python: Data collection, analysis, and visualization
- APIs: Spotipy (Spotify), Requests (Census)
- Analysis: Pandas, NumPy for data manipulation
- Visualization: Plotly (interactive), Matplotlib/Seaborn (static)
- Geographic Analysis: Choropleth maps, state-level correlations
- Deployment: Streamlit Cloud for live dashboard
- Version Control: Git/GitHub for project management

## Key Visualizations

1. **Interactive US Map**: Choropleth visualization of Indian population density with hover details
2. **Music Category Rankings**: State-by-state rankings with color-coded preference patterns
3. **Business Intelligence Dashboard**: Market opportunity vs content gap analysis
4. **Cultural Pattern Analysis**: Income vs music diversity correlation

## Skills Demonstrated

### Data Engineering
- Multi-source API integration and data pipeline development
- Data cleaning, validation, and quality assurance processes
- ETL pipeline design for reproducible analysis

### Statistical Analysis
- Correlation analysis between demographic and cultural variables
- Geographic clustering and pattern recognition
- Descriptive statistics and trend identification

### Data Visualization
- Interactive dashboard creation with Plotly
- Geographic data visualization (choropleth maps)
- Multi-panel analytical dashboards

### Business Intelligence
- Market opportunity identification and quantification
- Strategic recommendation development
- Stakeholder-ready presentation materials

## Project Structure
indian-music-analysis/
├── data/
│   ├── raw/
│   │   └── spotify_indian_playlists.csv
│   └── processed/
│       ├── us_indian_demographics.csv
│       ├── state_music_rankings.csv
│       └── regional_analysis_summary.csv
├── notebooks/
|   ├── 00_project_setup_test.ipynb
│   ├── 01_indian_music_data_collection.ipynb
│   └── 02_regional_demographic_analysis.ipynb
├── src/
│   └── app.py
└── requirements.txt

  # Key Achievements

| Metric | Value | Description |
|--------|-------|-------------|
| Data Points | 4.4M+ | Indian Americans analyzed across demographics |
| Playlists | 235+ | Music playlists analyzed across categories |
| Geographic Coverage | 15 states | Top markets by Indian population |
| API Integrations | 2 | Spotify + US Census data sources |
| Visualizations | 12+ | Interactive charts and analytics |
| Business Insights | 20+ | Strategic recommendations generated |

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Git
- Spotify Developer Account
- US Census API Key

### Installation
```bash
git clone https://github.com/JoshnaPR/Indian-music-analysis.git
cd indian-music-analysis
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Running the Analysis
  jupyter notebook
# Run notebooks in order: 00, 01, 02

# For local dashboard:
cd src
streamlit run app.py

### Contact Information
Developer: Joshna Prasanna Raghavan
Email: joshna.p2507@gmail.com
GitHub: https://github.com/JoshnaPR
Live Dashboard: https://indian-music-analysis-joshnapr.streamlit.app/
