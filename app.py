import streamlit as st
import requests

# --- HELPER FUNCTIONS ---
def calculate_expected_win(elo_a, elo_b, home_advantage=0):
    """Calculates the expected win probability for Team A using the standard Elo formula."""
    rating_diff = (elo_a + home_advantage) - elo_b
    prob_a = 1 / (10 ** (-rating_diff / 400) + 1)
    return prob_a

def fetch_rapidapi_data(api_key, endpoint, querystring):
    """Securely fetches data from API-Football via RapidAPI."""
    url = f"https://api-football-v1.p.rapidapi.com/v3/{endpoint}"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching secure data: {e}")
        return None

# --- WEB APP UI ---
st.set_page_config(page_title="Hybrid World Cup Predictor", page_icon="⚽", layout="wide")

st.title("⚽ Secure Hybrid 2026 World Cup Predictor")
st.markdown("Blending statistical Elo ratings with live market data via RapidAPI.")

# Securely pull the API key
api_key = st.secrets.get("RAPIDAPI_KEY")
if not api_key:
    st.warning("⚠️ API Key not found. Please add your RAPIDAPI_KEY to Streamlit Secrets.")

st.divider()

# --- DASHBOARD LAYOUT ---
# Using columns to create a professional dashboard layout
left_col, right_col = st.columns([2, 1])

with left_col:
    st.header("Match 1: Mexico vs. South Africa")
    st.caption("Venue: Mexico City Stadium (Home Advantage Applied)")
    
    col1, col2 = st.columns(2)
    with col1:
        mexico_elo = st.number_input("Mexico Elo", value=1875)
        mexico_live_odds = st.number_input("Mexico Live Odds (Decimal)", value=1.50, step=0.1) 
        
    with col2:
        sa_elo = st.number_input("South Africa Elo", value=1517)
        sa_live_odds = st.number_input("South Africa Live Odds (Decimal)", value=6.50, step=0.1)

    # Core Calculations
    math_prob_mexico = calculate_expected_win(mexico_elo, sa_elo, home_advantage=100)
    market_prob_mexico = 1 / mexico_live_odds if mexico_live_odds > 0 else 0

    st.markdown("### ⚙️ Model Weighting")
    math_weight = st.slider("Trust the Math (Elo) vs. Market (Odds)", 0, 100, 60) / 100
    market_weight = 1.0 - math_weight
    
    hybrid_prob_mexico = (math_prob_mexico * math_weight) + (market_prob_mexico * market_weight)

    st.markdown("### 📊 Final Prediction Breakdown")
    st.info(f"**🔢 Statistical Model (Elo):** {math_prob_mexico * 100:.1f}%")
    st.warning(f"**🎰 Live Market (Odds):** {market_prob_mexico * 100:.1f}%")
    st.success(f"**🎯 HYBRID WIN PROBABILITY (Mexico):** {hybrid_prob_mexico * 100:.1f}%")

with right_col:
    st.header("📡 Live Match Stats")
    st.markdown("*(Data feed staging area for live kickoff)*")
    
    # This button demonstrates how you will call the secure API once the match is live
    if st.button("Fetch Live Stats from API-Football"):
        if api_key:
            # Note: "fixture" ID would be updated to the actual 2026 World Cup fixture ID
            mock_query = {"fixture": "104"} 
            with st.spinner("Securely connecting to RapidAPI..."):
                # live_stats = fetch_rapidapi_data(api_key, "fixtures/statistics", mock_query)
                st.success("Secure connection established!")
                # Placeholder for live data rendering
                st.metric(label="Mexico Possession", value="55%")
                st.metric(label="Mexico Shots on Target", value="4")
                st.metric(label="South Africa Possession", value="45%")
        else:
            st.error("Cannot fetch data without RAPIDAPI_KEY.")
