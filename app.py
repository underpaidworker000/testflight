import streamlit as st

# --- HELPER FUNCTIONS ---
def calculate_expected_win(elo_a, elo_b, home_advantage=0):
    """
    Calculates the expected win probability for Team A using the standard Elo formula.
    """
    rating_diff = (elo_a + home_advantage) - elo_b
    prob_a = 1 / (10 ** (-rating_diff / 400) + 1)
    prob_b = 1 - prob_a
    return prob_a, prob_b

# --- WEB APP UI ---
st.set_page_config(page_title="World Cup Predictor", page_icon="⚽", layout="centered")

st.title("⚽ 2026 FIFA World Cup Predictor")
st.markdown("Adjust the Elo ratings below to calculate the real-time win probability for any matchup.")

st.divider()

# --- MATCH 1: Mexico vs South Africa ---
st.header("Match 1: Mexico vs. South Africa")
st.caption("Venue: Mexico City Stadium (Home Advantage Applied)")

col1, col2 = st.columns(2)

with col1:
    mexico_elo = st.number_input("Mexico Elo", value=1875)
    mex_home_adv = st.slider("Mexico Home Advantage Points", 0, 150, 100)

with col2:
    sa_elo = st.number_input("South Africa Elo", value=1517)

# Calculate Match 1
prob_mex, prob_sa = calculate_expected_win(mexico_elo, sa_elo, home_advantage=mex_home_adv)

st.success(f"**Prediction:** Mexico has a **{prob_mex * 100:.1f}%** chance of winning.")
st.error(f"**Prediction:** South Africa has a **{prob_sa * 100:.1f}%** chance of winning.")

st.divider()

# --- MATCH 2: South Korea vs Czechia ---
st.header("Match 2: South Korea vs. Czechia")
st.caption("Venue: Estadio Guadalajara (Neutral Venue)")

col3, col4 = st.columns(2)

with col3:
    korea_elo = st.number_input("South Korea Elo", value=1758)

with col4:
    czechia_elo = st.number_input("Czechia Elo", value=1740)

# Calculate Match 2 (No home advantage)
prob_kor, prob_cze = calculate_expected_win(korea_elo, czechia_elo, home_advantage=0)

st.success(f"**Prediction:** South Korea has a **{prob_kor * 100:.1f}%** chance of winning.")
st.info(f"**Prediction:** Czechia has a **{prob_cze * 100:.1f}%** chance of winning.")

st.divider()
st.markdown("*Probabilities sum to 100%. In knockout stages, this represents the chance to advance. In group stages, a portion of this probability represents the chance of a draw.*")
