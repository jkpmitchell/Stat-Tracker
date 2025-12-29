# This module will contain functions to plot various types of graphs and visualizations for data analysis.

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_stat_over_time(df, stat, player_name, rolling_window=5):
    """Plot a stat over time with rolling average"""
    df = df.sort_values('date')
    df['date'] = pd.to_datetime(df['date'])
    
    plt.figure(figsize=(12, 6))
    
    # Plot actual values
    plt.plot(df['date'], df[stat], 'o-', alpha=0.5, label=f'Game-by-game {stat}')
    
    # Plot rolling average
    rolling_avg = df[stat].rolling(window=rolling_window, min_periods=1).mean()
    plt.plot(df['date'], rolling_avg, 'r-', linewidth=2, label=f'{rolling_window}-game average')
    
    plt.title(f'{player_name} - {stat.upper()} Over Time')
    plt.xlabel('Date')
    plt.ylabel(stat.upper())
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def compare_players_chart(df1, df2, stat, name1, name2):
    """Bar chart comparing two players"""
    avg1 = df1[stat].mean()
    avg2 = df2[stat].mean()
    
    plt.figure(figsize=(8, 6))
    plt.bar([name1, name2], [avg1, avg2], color=['blue', 'red'], alpha=0.7)
    plt.title(f'{stat.upper()} Comparison')
    plt.ylabel(stat.upper())
    
    # Add value labels on bars
    plt.text(0, avg1 + 0.01, f'{avg1:.3f}', ha='center')
    plt.text(1, avg2 + 0.01, f'{avg2:.3f}', ha='center')
    
    plt.tight_layout()
    plt.show()

def plot_multiple_stats(df, stats, player_name):
    """Plot multiple stats in subplots"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f'{player_name} - Multiple Stats', fontsize=16)
    
    df = df.sort_values('date')
    df['date'] = pd.to_datetime(df['date'])
    
    for i, stat in enumerate(stats[:4]):
        ax = axes[i//2, i%2]
        if stat in df.columns:
            rolling_avg = df[stat].rolling(window=5, min_periods=1).mean()
            ax.plot(df['date'], rolling_avg, 'o-')
            ax.set_title(f'{stat.upper()}')
            ax.set_xlabel('Date')
            ax.set_ylabel(stat.upper())
            ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()