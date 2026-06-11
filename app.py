import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# The rest of your code starts here...
st.divider()
st.subheader("📡 Live Match Stats (API-Football)")

# The Engine: Function to fetch live matches from RapidAPI
def fetch_live_matches(api_key):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    # The 'live=all' parameter tells the API to only return games happening right now
    querystring = {"live": "all"} 
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        return data.get("response", [])
    except Exception as e:
        st.error(f"Failed to connect to RapidAPI: {e}")
        return []

# Execute the search
if st.button("🔄 Refresh Live Data"):
    with st.spinner("Fetching live World Cup data..."):
        live_games = fetch_live_matches(api_key)
        
        if not live_games:
            st.warning("No live matches found at this exact moment. Check back closer to kickoff!")
        else:
            # Loop through the live games and display the scores
            for game in live_games:
                home_team = game['teams']['home']['name']
                away_team = game['teams']['away']['name']
                home_goals = game['goals']['home']
                away_goals = game['goals']['away']
                elapsed_time = game['fixture']['status']['elapsed']
                
                st.success(f"⏱️ {elapsed_time}' | **{home_team} {home_goals} - {away_goals} {away_team}**")
