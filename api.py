"""
Flask API for Fantasy Basketball Manager
Provides REST endpoints for the Next.js frontend
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from data_fetcher import NBADataFetcher
from game_predictor import NBAGamePredictor

app = Flask(__name__)
CORS(app)  # Enable CORS for Next.js frontend

# Initialize services
fetcher = NBADataFetcher()
predictor = NBAGamePredictor()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'Fantasy Basketball API'})


@app.route('/api/player/stats/<player_name>', methods=['GET'])
def get_player_stats(player_name):
    """Get player season statistics."""
    try:
        stats = fetcher.get_player_stats(player_name)
        
        if stats.empty:
            return jsonify({'error': 'Player not found'}), 404
        
        # Convert DataFrame to dict
        player_data = stats.iloc[0].to_dict()
        
        return jsonify({
            'player_name': player_data['PLAYER_NAME'],
            'team': player_data['TEAM_ABBREVIATION'],
            'stats': {
                'ppg': float(player_data['PTS']),
                'rpg': float(player_data['REB']),
                'apg': float(player_data['AST']),
                'spg': float(player_data['STL']),
                'bpg': float(player_data['BLK']),
                'fg_pct': float(player_data['FG_PCT']),
                'ft_pct': float(player_data['FT_PCT']),
                'fg3_pct': float(player_data['FG3_PCT']),
                'minutes': float(player_data['MIN']),
                'games_played': int(player_data['GP'])
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/player/predict/<player_name>', methods=['GET'])
def predict_player(player_name):
    """Predict player performance."""
    try:
        prediction = predictor.predict_player_performance(player_name)
        
        if 'error' in prediction:
            return jsonify(prediction), 404
        
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/game/predict', methods=['POST'])
def predict_game():
    """Predict game outcome."""
    try:
        data = request.json
        home_team = data.get('home_team')
        away_team = data.get('away_team')
        
        if not home_team or not away_team:
            return jsonify({'error': 'Missing team parameters'}), 400
        
        prediction = predictor.predict_game_winner(home_team, away_team)
        
        if 'error' in prediction:
            return jsonify(prediction), 404
        
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/matchup/analyze', methods=['POST'])
def analyze_matchup():
    """Analyze player vs opponent matchup."""
    try:
        data = request.json
        player_name = data.get('player_name')
        opponent = data.get('opponent')
        
        if not player_name or not opponent:
            return jsonify({'error': 'Missing parameters'}), 400
        
        analysis = predictor.analyze_matchup(player_name, opponent)
        
        if 'error' in analysis:
            return jsonify(analysis), 404
        
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/leaders/<stat_category>', methods=['GET'])
def get_leaders(stat_category):
    """Get league leaders in a stat category."""
    try:
        top_n = request.args.get('limit', 20, type=int)
        leaders = fetcher.get_league_leaders(stat_category.upper(), top_n)
        
        if leaders.empty:
            return jsonify({'error': 'Invalid stat category'}), 400
        
        # Convert to list of dicts
        leaders_list = leaders.to_dict('records')
        
        return jsonify({
            'category': stat_category,
            'leaders': leaders_list
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
