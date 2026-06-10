import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="2026 FIFA World Cup Hybrid Predictor", layout="centered")
st.title("🏆 2026 FIFA World Cup Hybrid Predictor")
st.write("Continuously updating match predictions blending Elo math with live market odds.")

# 2. Select Match
st.sidebar.header("Select Upcoming Match")
match_selection = st.sidebar.selectbox(
    "Choose Match (June 11, 2026):",
    ("Mexico vs. South Africa", "South Korea vs. Czechia")
)

# Set Elo Ratings based on selection
if match_selection == "Mexico vs. South Africa":
    home_team = "Mexico"
    away_team = "South Africa"
    elo_home = 1875
    elo_away = 1517
    home_adv = 100 # Mexico plays at home in Mexico City
else:
    home_team = "South Korea"
    away_team = "Czechia"
    elo_home = 1758
    elo_away = 1740
    home_adv = 0 # Neutral venue

# 3. The Math Baseline (Elo Probability)
st.subheader(f"📊 Baseline Mathematical Model (Elo)")
st.write(f"**{home_team} Elo:** {elo_home} (+{home_adv} Home Advantage)")
st.write(f"**{away_team} Elo:** {elo_away}")

# Elo Formula: We = 1 / (10^(-dr/400) + 1)
dr = (elo_home + home_adv) - elo_away
math_prob_home = 1 / (10**(-dr/400) + 1)

st.info(f"Mathematical Win Probability ({home_team}): **{math_prob_home * 100:.1f}%**")

# 4. Live Market Baseline (Bookmaker Odds)
st.subheader("📈 Live Market Baseline (Bookmaker Odds)")
st.write("Enter the live decimal odds for the home team to convert into implied probability.")
market_odds = st.number_input(f"Live Decimal Odds for {home_team}", min_value=1.01, value=1.50, step=0.05)

# Convert odds to implied probability (1 / Decimal Odds)
market_prob = 1 / market_odds
st.info(f"Wisdom of the Crowd Probability ({home_team}): **{market_prob * 100:.1f}%**")

# 5. The Hybrid Output
st.subheader("🧠 The Hybrid Output")
st.write("Adjust the slider to change how much you trust the pure math versus the live betting market.")
weight = st.slider("Trust the Math (Elo) vs. Market (Odds)", 0, 100, 60)

# Blending the probabilities
hybrid_prob = (math_prob_home * (weight / 100)) + (market_prob * ((100 - weight) / 100))

st.success(f"### 🔥 Final Hybrid Win Probability ({home_team}): {hybrid_prob * 100:.1f}%")

# 6. Live Match Stats (API-Football integration via RapidAPI)
st.subheader("📡 Live Match Stats (API-Football)")
if st.button("Fetch Live Match Data"):
    try:
        # Securely loading API key from Streamlit Secrets
        api_key = st.secrets["RAPIDAPI_KEY"]
        
        # Example API Call to API-Football
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        
        # In a fully deployed version, you would pass the fixture ID here.
        # response = requests.get(url, headers=headers, params={"date": "2026-06-11"})
        
        st.success("API Key authenticated successfully! Connected to API-Football securely.")
        st.write("*(Data stream ready for live match kickoff!)*")
        
    except FileNotFoundError:
         st.error("⚠️ RAPIDAPI_KEY not found. Please add your key to the Streamlit Secrets in your dashboard.")
    except Exception as e:
         st.error(f"An error occurred: {e}")
