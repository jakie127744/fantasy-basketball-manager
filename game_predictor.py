"""
NBA Game Predictor
Predicts game outcomes and player performance using ML
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
from typing import Dict, Tuple, List
import logging

from data_fetcher import NBADataFetcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NBAGamePredictor:
    """Predict NBA game outcomes and player performance."""
    
    def __init__(self):
        """Initialize the predictor."""
        self.fetcher = NBADataFetcher()
        self.win_predictor = None
        self.score_predictor = None
        self.scaler = StandardScaler()
        
    def extract_team_features(self, team_abbr: str) -> Dict:
        """
        Extract features for a team.
        
        Args:
            team_abbr: Team abbreviation (e.g., 'LAL')
            
        Returns:
            Dictionary of team features
        """
        # Get team stats
        stats = self.fetcher.get_league_leaders('PTS', 500)  # Get all players
        team_stats = stats[stats['TEAM_ABBREVIATION'] == team_abbr]
        
        if team_stats.empty:
            return {}
        
        features = {
            'avg_points': team_stats['PTS'].mean(),
            'total_minutes': team_stats['MIN'].sum(),
            'games_played': team_stats['GP'].mean(),
            'num_players': len(team_stats)
        }
        
        return features
    
    def predict_game_winner(self, home_team: str, away_team: str) -> Dict:
        """
        Predict game winner and probability.
        
        Args:
            home_team: Home team abbreviation
            away_team: Away team abbreviation
            
        Returns:
            Dictionary with prediction and probabilities
        """
        # Extract features for both teams
        home_features = self.extract_team_features(home_team)
        away_features = self.extract_team_features(away_team)
        
        if not home_features or not away_features:
            return {
                'error': 'Could not fetch team data',
                'home_team': home_team,
                'away_team': away_team
            }
        
        # Simple prediction based on average points
        home_avg = home_features['avg_points']
        away_avg = away_features['avg_points']
        
        # Add home court advantage (typically 3-4 points)
        home_advantage = 3.5
        home_score_estimate = home_avg + home_advantage
        away_score_estimate = away_avg
        
        # Calculate win probability
        point_diff = home_score_estimate - away_score_estimate
        home_win_prob = 1 / (1 + np.exp(-point_diff / 10))  # Logistic function
        
        prediction = {
            'home_team': home_team,
            'away_team': away_team,
            'predicted_winner': home_team if home_win_prob > 0.5 else away_team,
            'home_win_probability': home_win_prob,
            'away_win_probability': 1 - home_win_prob,
            'predicted_home_score': round(home_score_estimate, 1),
            'predicted_away_score': round(away_score_estimate, 1),
            'predicted_total': round(home_score_estimate + away_score_estimate, 1),
            'predicted_spread': round(point_diff, 1)
        }
        
        return prediction
    
    def predict_player_performance(self, player_name: str, opponent: str = None) -> Dict:
        """
        Predict player's performance in next game.
        
        Args:
            player_name: Player's name
            opponent: Opponent team (optional, for matchup analysis)
            
        Returns:
            Dictionary with predicted stats
        """
        # Get recent games
        recent_games = self.fetcher.get_recent_games(player_name, 10)
        
        if recent_games.empty:
            return {'error': f'No data found for {player_name}'}
        
        # Calculate averages from recent games
        prediction = {
            'player_name': player_name,
            'games_analyzed': len(recent_games),
            'predicted_points': round(recent_games['PTS'].mean(), 1),
            'predicted_rebounds': round(recent_games['REB'].mean(), 1),
            'predicted_assists': round(recent_games['AST'].mean(), 1),
            'predicted_steals': round(recent_games['STL'].mean(), 1),
            'predicted_blocks': round(recent_games['BLK'].mean(), 1),
            'predicted_turnovers': round(recent_games['TOV'].mean(), 1),
            'predicted_fg_pct': round(recent_games['FG_PCT'].mean(), 3),
            'predicted_minutes': round(recent_games['MIN'].mean(), 1),
            'consistency_score': round(1 - (recent_games['PTS'].std() / recent_games['PTS'].mean()), 2),
            'trending': 'up' if recent_games['PTS'].iloc[:3].mean() > recent_games['PTS'].iloc[3:].mean() else 'down'
        }
        
        # Calculate fantasy points (standard scoring)
        prediction['predicted_fantasy_points'] = round(
            prediction['predicted_points'] +
            prediction['predicted_rebounds'] * 1.2 +
            prediction['predicted_assists'] * 1.5 +
            prediction['predicted_steals'] * 3 +
            prediction['predicted_blocks'] * 3 -
            prediction['predicted_turnovers'],
            1
        )
        
        return prediction
    
    def predict_over_under(self, home_team: str, away_team: str) -> Dict:
        """
        Predict if game will go over/under betting line.
        
        Args:
            home_team: Home team abbreviation
            away_team: Away team abbreviation
            
        Returns:
            Dictionary with over/under prediction
        """
        game_pred = self.predict_game_winner(home_team, away_team)
        
        if 'error' in game_pred:
            return game_pred
        
        predicted_total = game_pred['predicted_total']
        
        # Typical NBA total is around 220
        typical_total = 220
        
        return {
            'home_team': home_team,
            'away_team': away_team,
            'predicted_total': predicted_total,
            'recommendation': 'OVER' if predicted_total > typical_total else 'UNDER',
            'confidence': abs(predicted_total - typical_total) / 10  # Simple confidence metric
        }
    
    def analyze_matchup(self, player_name: str, opponent_team: str) -> Dict:
        """
        Analyze player's historical performance vs specific opponent.
        
        Args:
            player_name: Player's name
            opponent_team: Opponent team abbreviation
            
        Returns:
            Dictionary with matchup analysis
        """
        # Get all recent games
        all_games = self.fetcher.get_recent_games(player_name, 50)
        
        if all_games.empty:
            return {'error': f'No data found for {player_name}'}
        
        # Filter games vs this opponent
        matchup_games = all_games[all_games['MATCHUP'].str.contains(opponent_team)]
        
        if matchup_games.empty:
            return {
                'player_name': player_name,
                'opponent': opponent_team,
                'note': 'No recent games vs this opponent',
                'use_overall_average': True
            }
        
        analysis = {
            'player_name': player_name,
            'opponent': opponent_team,
            'games_vs_opponent': len(matchup_games),
            'avg_points_vs_opponent': round(matchup_games['PTS'].mean(), 1),
            'avg_points_overall': round(all_games['PTS'].mean(), 1),
            'performance_diff': round(matchup_games['PTS'].mean() - all_games['PTS'].mean(), 1),
            'favorable_matchup': matchup_games['PTS'].mean() > all_games['PTS'].mean()
        }
        
        return analysis


if __name__ == "__main__":
    # Test the game predictor
    predictor = NBAGamePredictor()
    
    print("NBA Game Predictor - Testing")
    print("=" * 60)
    
    # Test 1: Predict game winner
    print("\n1. Game Prediction: Lakers vs Celtics")
    game_pred = predictor.predict_game_winner('LAL', 'BOS')
    for key, value in game_pred.items():
        print(f"  {key}: {value}")
    
    # Test 2: Player performance prediction
    print("\n2. Player Performance: LeBron James")
    player_pred = predictor.predict_player_performance("LeBron James")
    for key, value in player_pred.items():
        print(f"  {key}: {value}")
    
    # Test 3: Over/Under prediction
    print("\n3. Over/Under: Warriors vs Suns")
    ou_pred = predictor.predict_over_under('GSW', 'PHX')
    for key, value in ou_pred.items():
        print(f"  {key}: {value}")
    
    # Test 4: Matchup analysis
    print("\n4. Matchup Analysis: Stephen Curry vs Lakers")
    matchup = predictor.analyze_matchup("Stephen Curry", "LAL")
    for key, value in matchup.items():
        print(f"  {key}: {value}")
