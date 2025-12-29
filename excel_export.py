# This module will allow for exporting data to Excel files for further analysis and sharing. 

import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
import os

def export_to_excel(df, player_name, filename=None):
    """Export player data to Excel with charts"""
    if filename is None:
        filename = f"exports/{player_name.replace(' ', '_')}_stats.xlsx"
    
    # Make sure exports directory exists
    os.makedirs('exports', exist_ok=True)
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Write main data
        df.to_excel(writer, sheet_name='Game Stats', index=False)
        
        # Calculate summary stats
        summary_stats = ['avg', 'obp', 'slg', 'ops', 'homeRuns', 'rbi']
        available_stats = [stat for stat in summary_stats if stat in df.columns]
        
        if available_stats:
            summary = df[available_stats].agg(['mean', 'max', 'min', 'std']).round(3)
            summary.to_excel(writer, sheet_name='Summary')
    
    print(f"Exported to {filename}")

def export_comparison(df1, df2, name1, name2, filename="exports/player_comparison.xlsx"):
    """Export comparison between two players"""
    os.makedirs('exports', exist_ok=True)
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Player 1 data
        df1.to_excel(writer, sheet_name=name1, index=False)
        
        # Player 2 data  
        df2.to_excel(writer, sheet_name=name2, index=False)
        
        # Comparison summary
        stats = ['avg', 'obp', 'slg', 'ops']
        comparison_data = []
        
        for stat in stats:
            if stat in df1.columns and stat in df2.columns:
                comparison_data.append({
                    'Stat': stat.upper(),
                    name1: df1[stat].mean(),
                    name2: df2[stat].mean()
                })
        
        comparison_df = pd.DataFrame(comparison_data)
        comparison_df.to_excel(writer, sheet_name='Comparison', index=False)
    
    print(f"Comparison exported to {filename}")