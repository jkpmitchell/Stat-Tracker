# A simple dashboard will be created using Streamlit to visualize the key metrics and insights derived from the baseball sabermetrics analysis.

import streamlit as st
import baseball_data
import stats_calculator
import plotter
import pandas as pd
import matplotlib.pyplot as plt

db_path = "C:/Users/wzhoo/OneDrive/Documents/Resume/Sabermetrics/database2.db"

st.title("⚾ Simple Baseball Dashboard")

# Sidebar for player selection
st.sidebar.header("Player Selection")
player_name = st.sidebar.text_input("Enter player name:")

if player_name:
    players = baseball_data.search_player(player_name)
    
    if players:
        # Select player
        player_options = [f"{p['name']} ({p['team']})" for p in players]
        selected_idx = st.sidebar.selectbox("Choose player:", range(len(player_options)), 
                                          format_func=lambda x: player_options[x])
        selected_player = players[selected_idx]
        
        # Days of data
        days = st.sidebar.slider("Days of data:", 7, 90, 30)
        
        # Get data
        with st.spinner("Getting player data..."):
            df = baseball_data.get_player_stats(selected_player['id'], days)
        
        if not df.empty:
            df = stats_calculator.calculate_advanced_stats(df)
            
            # Show basic info
            st.header(f"{selected_player['name']}")
            st.write(f"**Team:** {selected_player['team']}")
            st.write(f"**Games:** {len(df)}")
            
            # Key stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                df['avg'] = pd.to_numeric(df['avg'], errors='coerce')
                st.metric("Batting Avg", f"{df['avg'].mean():.3f}")
            with col2:
                df['obp'] = pd.to_numeric(df['obp'], errors='coerce')
                st.metric("OBP", f"{df['obp'].mean():.3f}")
            with col3:
                df['slg'] = pd.to_numeric(df['slg'], errors='coerce')
                st.metric("SLG", f"{df['slg'].mean():.3f}")
            with col4:
                df['ops'] = pd.to_numeric(df['ops'], errors='coerce')
                st.metric("OPS", f"{df['ops'].mean():.3f}")
            
            # Charts
            st.subheader("Performance Over Time")
            
            stat_to_plot = st.selectbox("Choose stat to plot:", ['avg', 'obp', 'slg', 'ops'])
            
            # Create chart
            df_sorted = df.sort_values('date')
            df_sorted['date'] = pd.to_datetime(df_sorted['date'])
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df_sorted['date'], df_sorted[stat_to_plot], 'o-', alpha=0.7)
            ax.set_title(f'{stat_to_plot.upper()} Over Time')
            ax.set_xlabel('Date')
            ax.set_ylabel(stat_to_plot.upper())
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            st.pyplot(fig)
            
            # Show recent games
            st.subheader("Recent Games")
            display_cols = ['date', 'avg', 'obp', 'slg', 'ops', 'homeRuns', 'rbi', 'hits', 'atBats']
            available_cols = [col for col in display_cols if col in df.columns]
            st.dataframe(df[available_cols].head(10))
        else:
            st.warning("No recent games found for this player.")
    else:
        st.warning("No players found with that name.")