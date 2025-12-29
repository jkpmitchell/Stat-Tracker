# This module is main script that will coordinate the overall functionality of the baseball sabermetrics analysis project.
#!/usr/bin/env python3

"""
Simple Baseball Stats Analysis
"""
import baseball_data
import stats_calculator
import plotter
import excel_export

def main():
    print("🏟️ Baseball Stats Analyzer")
    print("=" * 30)
    
    # Get player
    player_name = input("Enter player name: ")
    players = baseball_data.search_player(player_name)
    
    if not players:
        print("No players found!")
        return
    
    # Show options if multiple players
    if len(players) > 1:
        print("Multiple players found:")
        for i, player in enumerate(players):
            print(f"{i+1}. {player['name']} ({player['team']})")
        choice = int(input("Choose player (number): ")) - 1
        selected_player = players[choice]
    else:
        selected_player = players[0]
    
    print(f"Analyzing {selected_player['name']}...")
    
    # Get data
    days = int(input("How many days of data? (default 30): ") or 30)
    df = baseball_data.get_player_stats(selected_player['id'], days)
    
    if df.empty:
        print("No recent games found!")
        return
    
    # Calculate advanced stats
    df = stats_calculator.calculate_advanced_stats(df)
    
    # Save data
    baseball_data.save_data(df, f"{selected_player['name'].replace(' ', '_')}_games.csv")
    
    # Show menu
    while True:
        print("\nWhat would you like to do?")
        print("1. Plot OPS over time")
        print("2. Plot batting average over time") 
        print("3. Show multiple stats")
        print("4. Export to Excel")
        print("5. Quit")
        
        choice = input("Choose option (1-5): ")
        
        if choice == '1':
            plotter.plot_stat_over_time(df, 'ops', selected_player['name'])
        elif choice == '2':
            plotter.plot_stat_over_time(df, 'avg', selected_player['name'])
        elif choice == '3':
            plotter.plot_multiple_stats(df, ['avg', 'obp', 'slg', 'ops'], selected_player['name'])
        elif choice == '4':
            excel_export.export_to_excel(df, selected_player['name'])
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()