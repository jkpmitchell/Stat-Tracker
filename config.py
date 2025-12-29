#Simple config settings for the application.

# Simple configuration
MLB_API_URL = "https://statsapi.mlb.com/api/v1"

# Team abbreviations
TEAMS = {
    'CHW': 'Chicago White Sox',
    'PiTS': 'Pittsburgh Pirates',
# Add more as needed
}

# Stats we want to track
BASIC_STATS = ['atBats', 'hits', 'homeRuns', 'rbi', 'avg']
ADVANCED_STATS = ['obp', 'slg', 'ops']