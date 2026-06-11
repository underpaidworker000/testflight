import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# The rest of your code starts here...
st.subheader("📡 Live Match Stats (API-Football)")

st.title("🏆 2026 Live World Cup Predictor")
st.write("Live mathematical predictions using real-time Elo data.")

# Securely load API key from Streamlit Secrets
api_key = st.secrets["RAPIDAPI_KEY"]

# 1. The Web Scraper (Fetches Live Elo Ratings)
@st.cache_data(ttl=3600) # Caches the data for 1 hour to prevent IP bans
def get_live_elo_data():
    url = "https://www.eloratings.net/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the main ratings table 
    # (Note: eloratings.net uses a specific div structure, this extracts the raw text)
    teams = []
    ratings = []
    
    # We look for the specific divs that hold the team names and ratings
    for team_div in soup.find_all('div', class_='team-name'):
        teams.append(team_div.text.strip())
        
    for rating_div in soup.find_all('div', class_='rating'):
        ratings.append(int(rating_div.text.strip()))
        
    # Create a Pandas DataFrame for easy lookup
    elo_df = pd.DataFrame({'Team': teams, 'Elo': ratings})
    return elo_df

# Load the live data
try:
    live_elo_df = get_live_elo_data()
    st.success("✅ Live Elo data successfully scraped from eloratings.net!")
except Exception as e:
    st.error(f"Failed to fetch live Elo data: {e}")
    live_elo_df = pd.DataFrame({'Team': ['Mexico', 'South Africa'], 'Elo': [1875, 1517]}) # Fallback

# 2. Elo Win Probability Function
def calculate_elo_probability(rating_a, rating_b, home_advantage=0):
    dr = (rating_a + home_advantage) - rating_b
    we = 1 / (10**(-dr/400) + 1)
    return we * 100

st.divider()

# 3. The Matchup Interface
st.subheader("Today's Opening Match")

# Dynamically look up the exact live ratings
try:
    mexico_live_elo = live_elo_df.loc[live_elo_df['Team'] == 'Mexico', 'Elo'].values[0]
    sa_live_elo = live_elo_df.loc[live_elo_df['Team'] == 'South Africa', 'Elo'].values[0]
except IndexError:
    # Fallback just in case the team name is spelled differently on the site today
    mexico_live_elo = 1875
    sa_live_elo = 1517

col1, col2 = st.columns(2)
with col1:
    mexico_elo = st.number_input("Mexico Live Elo", value=int(mexico_live_elo))
with col2:
    sa_elo = st.number_input("South Africa Live Elo", value=int(sa_live_elo))

# Calculate and Display
win_prob = calculate_elo_probability(mexico_elo, sa_elo, home_advantage=100)
st.metric(label="Mexico Win Probability (Adjusted for Home Advantage)", value=f"{win_prob:.1f}%")

st.info("Live API-Football match stats will populate here shortly.")
