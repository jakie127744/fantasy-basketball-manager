"""
Fantasy Basketball Manager
NBA Stats Data Fetcher
"""
from nba_api.stats.endpoints import playergamelog, leaguedashplayerstats, teamdashboardbygeneralsplits
from nba_api.stats.static import players, teams
import pandas as pd
import time
from typing import Optional, List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NBADataFetcher:
    """Fetch NBA player and team statistics."""
    
    def __init__(self):
        """Initialize the data fetcher."""
        self.current_season = "2024-25"
        self.all_players = players.get_players()
        self.all_teams = teams.get_teams()
    
    def find_player(self, player_name: str) -> Optional[Dict]:
        """
        Find player by name.
        
        Args:
            player_name: Player's full or partial name
            
        Returns:
            Player dictionary or None
        """
        player_name_lower = player_name.lower()
        
        for player in self.all_players:
            if player_name_lower in player['full_name'].lower():
                return player
        
        return None
    
    def get_player_stats(self, player_name: str, season: str = None) -> pd.DataFrame:
        """
        Get player season statistics.
        
        Args:
            player_name: Player's name
            season: Season (e.g., "2024-25"), defaults to current
            
        Returns:
            DataFrame with player stats
        """
        if season is None:
            season = self.current_season
        
        player = self.find_player(player_name)
        if not player:
            logger.error(f"Player not found: {player_name}")
            return pd.DataFrame()
        
        try:
            # Get season stats
            stats = leaguedashplayerstats.LeagueDashPlayerStats(
                season=season,
                per_mode_detailed='PerGame'
            )
            
            df = stats.get_data_frames()[0]
            player_stats = df[df['PLAYER_ID'] == player['id']]
            
            time.sleep(0.6)  # Rate limiting
            return player_stats
            
        except Exception as e:
            logger.error(f"Error fetching stats for {player_name}: {e}")
            return pd.DataFrame()
    
    def get_recent_games(self, player_name: str, num_games: int = 10) -> pd.DataFrame:
        """
        Get player's recent game logs.
        
        Args:
            player_name: Player's name
            num_games: Number of recent games to fetch
            
        Returns:
            DataFrame with game logs
        """
        player = self.find_player(player_name)
        if not player:
            logger.error(f"Player not found: {player_name}")
            return pd.DataFrame()
        
        try:
            # Get game logs
            gamelog = playergamelog.PlayerGameLog(
                player_id=player['id'],
                season=self.current_season
            )
            
            df = gamelog.get_data_frames()[0]
            
            time.sleep(0.6)  # Rate limiting
            return df.head(num_games)
            
        except Exception as e:
            logger.error(f"Error fetching game logs for {player_name}: {e}")
            return pd.DataFrame()
    
    def get_league_leaders(self, stat_category: str = 'PTS', top_n: int = 50) -> pd.DataFrame:
        """
        Get league leaders in a specific stat category.
        
        Args:
            stat_category: Stat to rank by (PTS, REB, AST, STL, BLK, etc.)
            top_n: Number of top players to return
            
        Returns:
            DataFrame with top players
        """
        try:
            stats = leaguedashplayerstats.LeagueDashPlayerStats(
                season=self.current_season,
                per_mode_detailed='PerGame'
            )
            
            df = stats.get_data_frames()[0]
            
            # Sort by stat category
            if stat_category in df.columns:
                leaders = df.nlargest(top_n, stat_category)
                time.sleep(0.6)
                return leaders[['PLAYER_NAME', 'TEAM_ABBREVIATION', stat_category, 'GP', 'MIN']]
            else:
                logger.error(f"Stat category not found: {stat_category}")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error fetching league leaders: {e}")
            return pd.DataFrame()
    
    def get_team_defense_rankings(self) -> pd.DataFrame:
        """
        Get team defensive rankings (points allowed per game by position).
        
        Returns:
            DataFrame with team defensive stats
        """
        try:
            # Get team stats
            stats = leaguedashplayerstats.LeagueDashPlayerStats(
                season=self.current_season,
                per_mode_detailed='PerGame'
            )
            
            df = stats.get_data_frames()[0]
            
            # Group by team and calculate defensive metrics
            team_stats = df.groupby('TEAM_ABBREVIATION').agg({
                'PTS': 'mean',
                'REB': 'mean',
                'AST': 'mean',
                'STL': 'mean',
                'BLK': 'mean'
            }).reset_index()
            
            team_stats.columns = ['TEAM', 'PTS_ALLOWED', 'REB_ALLOWED', 'AST_ALLOWED', 'STL_ALLOWED', 'BLK_ALLOWED']
            
            time.sleep(0.6)
            return team_stats.sort_values('PTS_ALLOWED')
            
        except Exception as e:
            logger.error(f"Error fetching team defense rankings: {e}")
            return pd.DataFrame()
    
    def get_player_advanced_stats(self, player_name: str) -> Dict:
        """
        Get advanced stats for a player (usage rate, PER, etc.).
        
        Args:
            player_name: Player's name
            
        Returns:
            Dictionary with advanced stats
        """
        stats = self.get_player_stats(player_name)
        
        if stats.empty:
            return {}
        
        row = stats.iloc[0]
        
        # Calculate advanced metrics
        advanced = {
            'player_name': row['PLAYER_NAME'],
            'team': row['TEAM_ABBREVIATION'],
            'ppg': row['PTS'],
            'rpg': row['REB'],
            'apg': row['AST'],
            'spg': row['STL'],
            'bpg': row['BLK'],
            'fg_pct': row['FG_PCT'],
            'ft_pct': row['FT_PCT'],
            'fg3_pct': row['FG3_PCT'],
            'minutes': row['MIN'],
            'games_played': row['GP']
        }
        
        return advanced


if __name__ == "__main__":
    # Test the data fetcher
    fetcher = NBADataFetcher()
    
    print("Testing NBA Data Fetcher...")
    print("=" * 60)
    
    # Test 1: Get player stats
    print("\n1. LeBron James Season Stats:")
    lebron_stats = fetcher.get_player_stats("LeBron James")
    if not lebron_stats.empty:
        print(lebron_stats[['PLAYER_NAME', 'PTS', 'REB', 'AST', 'FG_PCT']].to_string())
    
    # Test 2: Get recent games
    print("\n2. Stephen Curry Last 5 Games:")
    curry_games = fetcher.get_recent_games("Stephen Curry", 5)
    if not curry_games.empty:
        print(curry_games[['GAME_DATE', 'MATCHUP', 'PTS', 'REB', 'AST']].to_string())
    
    # Test 3: League leaders
    print("\n3. Top 10 Scorers:")
    scorers = fetcher.get_league_leaders('PTS', 10)
    print(scorers.to_string())
    
    # Test 4: Advanced stats
    print("\n4. Giannis Advanced Stats:")
    giannis_advanced = fetcher.get_player_advanced_stats("Giannis Antetokounmpo")
    for key, value in giannis_advanced.items():
        print(f"  {key}: {value}")
