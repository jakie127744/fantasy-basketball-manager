export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-500 to-purple-600">
      <main className="container mx-auto px-4 py-16">
        <div className="text-center text-white">
          <h1 className="text-6xl font-bold mb-4">
            🏀 Fantasy Basketball Manager
          </h1>
          <p className="text-2xl mb-8">
            AI-Powered NBA Analytics & Predictions
          </p>
          
          <div className="grid md:grid-cols-3 gap-8 mt-16">
            <div className="bg-white/10 backdrop-blur-lg rounded-lg p-8">
              <h2 className="text-3xl font-bold mb-4">📊 Real-Time Stats</h2>
              <p className="text-lg">
                Live NBA player statistics, game logs, and league leaders
              </p>
            </div>
            
            <div className="bg-white/10 backdrop-blur-lg rounded-lg p-8">
              <h2 className="text-3xl font-bold mb-4">🔮 Game Predictions</h2>
              <p className="text-lg">
                Win probability, score predictions, and betting insights
              </p>
            </div>
            
            <div className="bg-white/10 backdrop-blur-lg rounded-lg p-8">
              <h2 className="text-3xl font-bold mb-4">🎯 Player Analysis</h2>
              <p className="text-lg">
                Performance predictions and matchup analysis
              </p>
            </div>
          </div>
          
          <div className="mt-16">
            <p className="text-xl opacity-80">
              Coming Soon: Full analytics dashboard
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
