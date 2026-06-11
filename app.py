# 6. Live Match Stats (API-Football integration via RapidAPI)
st.subheader("📡 Live Match Stats (API-Football)")

if st.button("Fetch Live Match Data"):
    try:
        # Securely loading API key from Streamlit Secrets
        api_key = st.secrets["RAPIDAPI_KEY"]
        
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        
        # 1. Target the 2026 World Cup (League ID 1) and filter for live matches ('LIVE')
        # Note: You can also search by date if preferred: {"date": "2026-06-11", "league": "1"}
        querystring = {"league": "1", "season": "2026", "live": "all"}
        
        with st.spinner("Fetching live data from API-Football..."):
            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()
        
        if response.status_code == 200 and "response" in data and len(data["response"]) > 0:
            fixtures = data["response"]
            match_found = False
            
            # 2. Iterate through live fixtures to find the user's selected match
            for fixture in fixtures:
                api_home = fixture["teams"]["home"]["name"]
                api_away = fixture["teams"]["away"]["name"]
                
                # Check if this fixture matches our UI selection
                if home_team.lower() in api_home.lower() or away_team.lower() in api_away.lower():
                    match_found = True
                    
                    # Extract status and goals
                    status = fixture["fixture"]["status"]["long"]
                    elapsed = fixture["fixture"]["status"]["elapsed"]
                    goals_home = fixture["goals"]["home"]
                    goals_away = fixture["goals"]["away"]
                    
                    # 3. Display live match card in Streamlit
                    st.success(f"### Match Status: {status} ({elapsed}')")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(label=api_home, value=goals_home if goals_home is not None else 0)
                    with col2:
                        st.markdown("<h2 style='text-align: center;'>VS</h2>", unsafe_logic=True)
                    with col3:
                        st.metric(label=api_away, value=goals_away if goals_away is not None else 0)
                    
                    # Optional: Add live match events if they exist
                    if fixture.get("events"):
                        st.write("**Match Events:**")
                        for event in fixture["events"]:
                            st.write(f"⏱️ {event['time']['elapsed']}' - {event['detail']} ({event['team']['name']})")
                    break
            
            if not match_found:
                st.warning(f"No active live match data found on the server right now for **{home_team} vs. {away_team}**.")
                st.info("💡 Note: If the match hasn't kicked off yet, change the API parameters from `live=all` to `date=2026-06-11` to view scheduled match details.")
                
        else:
            st.error("Could not retrieve live fixtures. Verify league parameters or check if any tournament matches are currently active.")
            
    except KeyError:
         st.error("⚠️ `RAPIDAPI_KEY` not found. Please add your key to your local `.streamlit/secrets.toml` file or your Streamlit Cloud dashboard.")
    except Exception as e:
         st.error(f"An error occurred: {e}")
