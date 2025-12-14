# Fantasy Basketball Manager

🏀 **AI-Powered Fantasy Basketball Analytics & Predictions**

Live Demo: [Coming Soon]

## Features

- 📊 **Real-time NBA Stats** - Player statistics, game logs, league leaders
- 🔮 **Game Predictions** - Win probability, score predictions, spreads
- 🎯 **Player Performance** - Next-game predictions with fantasy points
- ⚔️ **Matchup Analysis** - Historical performance vs specific opponents
- 💰 **Betting Insights** - Over/under recommendations
- 📈 **Trend Detection** - Hot/cold streak identification

## Tech Stack

**Frontend:**

- Next.js 16 (App Router)
- TypeScript
- Tailwind CSS
- React

**Backend:**

- Python Flask API
- NBA Stats API
- Machine Learning (scikit-learn)

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.10+
- npm or yarn

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/fantasy-basketball.git
cd fantasy-basketball

# Install Python dependencies
pip install -r requirements.txt

# Install Next.js dependencies
cd fantasy-bball-app
npm install

# Start the Flask API (in one terminal)
cd ..
python api.py

# Start the Next.js app (in another terminal)
cd fantasy-bball-app
npm run dev
```

Visit `http://localhost:3000`

## Deployment

### Deploy to Vercel

1. Push to GitHub
2. Import project in Vercel
3. Configure environment variables
4. Deploy!

The Python API will run as Vercel Serverless Functions.

## API Endpoints

- `GET /api/player/stats/:name` - Get player statistics
- `GET /api/player/predict/:name` - Predict player performance
- `POST /api/game/predict` - Predict game outcome
- `POST /api/matchup/analyze` - Analyze player vs opponent
- `GET /api/leaders/:category` - Get league leaders

## Environment Variables

```env
# Optional: Add API keys if using paid services
NBA_API_KEY=your_key_here
ODDS_API_KEY=your_key_here
```

## Features Roadmap

- [x] Player stats fetching
- [x] Game predictions
- [x] Player performance predictions
- [x] Matchup analysis
- [ ] H2H category analyzer
- [ ] DFS lineup optimizer
- [ ] Injury report integration
- [ ] Real-time betting odds
- [ ] User authentication
- [ ] Save favorite players
- [ ] Custom scoring systems

## Contributing

Contributions welcome! Please open an issue or PR.

## License

MIT

## Author

Built with ❤️ for fantasy basketball enthusiasts
