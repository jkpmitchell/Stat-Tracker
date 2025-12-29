# Sabermetrics will be calculated in this module, including batting average, on-base percentage, slugging percentage, and more.

import pandas as pd

def calculate_advanced_stats(df):
    """Add advanced stats to dataframe"""
    df = df.copy()
    df['sacrificeFlies'] = df.get('sacrificeFlies', 0)
    
    # On-base percentage
    df['obp'] = (df['hits'] + df['baseOnBalls'] + df['hitByPitch']) / (
        df['atBats'] + df['baseOnBalls'] + df['hitByPitch'] + df['sacrificeFlies']
    )
    
    # Slugging percentage
    singles = df['hits'] - df['doubles'] - df['triples'] - df['homeRuns']
    df['slg'] = (singles + 2*df['doubles'] + 3*df['triples'] + 4*df['homeRuns']) / df['atBats']
    
    # OPS
    df['ops'] = df['obp'] + df['slg']
    
    # Fill NaN values with 0
    df = df.fillna(0)
    
    return df

def get_rolling_average(df, stat, window=5):
    """Calculate rolling average for a stat"""
    df = df.sort_values('date')
    df[f'{stat}_rolling'] = df[stat].rolling(window=window, min_periods=1).mean()
    return df

def compare_players(player1_df, player2_df, stats=['avg', 'obp', 'slg', 'ops']):
    """Compare average stats between two players"""
    comparison = {}
    
    for stat in stats:
        if stat in player1_df.columns and stat in player2_df.columns:
            comparison[stat] = {
                'player1': player1_df[stat].mean(),
                'player2': player2_df[stat].mean()
            }
    
    return pd.DataFrame(comparison).T