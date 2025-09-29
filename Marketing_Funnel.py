//not currently working. see errors//
import React, { useState, useEffect } from 'react';
import { 
  MessageCircle, 
  Twitter, 
  Send, 
  Users, 
  TrendingUp, 
  Zap, 
  Target, 
  Bot, 
  Share2, 
  Eye, 
  Heart, 
  Repeat,
  Download,
  Settings,
  Play,
  Pause,
  BarChart3,
  Crown,
  Gift
} from 'lucide-react';

const ViralMarketingDashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [botStatus, setBotStatus] = useState({
    discord: { active: true, servers: 47, commands_used: 1247 },
    telegram: { active: true, subscribers: 3891, engagement_rate: 8.7 },
    twitter: { active: true, followers: 12847, viral_tweets: 3 }
  });
  
  const [funnelMetrics, setFunnelMetrics] = useState({
    total_impressions: 147283,
    click_through_rate: 4.2,
    conversion_rate: 2.8,
    revenue_generated: 28947
  });

  const [contentQueue, setContentQueue] = useState([
    { platform: 'twitter', type: 'viral_thread', scheduled: '2024-01-15 09:00', status: 'pending' },
    { platform: 'discord', type: 'market_signal', scheduled: '2024-01-15 09:30', status: 'pending' },
    { platform: 'telegram', type: 'exclusive_alpha', scheduled: '2024-01-15 10:00', status: 'pending' }
  ]);

  const viralStrategies = [
    {
      name: "FOMO Scarcity Hooks",
      description: "Create urgency with limited-time offers and exclusive access",
      platforms: ["Twitter", "Discord", "Telegram"],
      conversion_rate: "12.4%",
      status: "active",
      examples: [
        "⏰ Only 23 spots left for premium access",
        "🔥 Alpha leak expires in 2 hours",
        "🚨 Early bird pricing ends tonight"
      ]
    },
    {
      name: "Social Proof Amplification", 
      description: "Showcase community wins and testimonials",
      platforms: ["All platforms"],
      conversion_rate: "8.7%",
      status: "active",
      examples: [
        "📈 Community member just hit +340% on our signal",
        "🏆 87% win rate this month",
        "👥 1,247 active traders using our system"
      ]
    },
    {
      name: "Exclusive Alpha Leaks",
      description: "Share premium insights to drive subscriptions",
      platforms: ["Telegram", "Discord"],
      conversion_rate: "15.2%", 
      status: "active",
      examples: [
        "🤫 Whale accumulation detected in mystery stock",
        "🔐 Premium members saw this move 48hrs early",
        "💎 Insider pattern forming in top 3 positions"
      ]
    }
  ];

  const AutomationCard = ({ platform, icon: Icon, metrics, status }) => (
    <div className="bg-white rounded-lg p-6 border border-gray-200 shadow-sm">
      <div className="mt-6 grid grid-cols-2 gap-4">
        <div className="text-center p-3 bg-gray-50 rounded">
          <div className="text-2xl font-bold text-green-600">${funnelMetrics.revenue_generated.toLocaleString()}</div>
          <div className="text-xs text-gray-500">Revenue Generated</div>
        </div>
        <div className="text-center p-3 bg-gray-50 rounded">
          <div className="text-2xl font-bold text-blue-600">{funnelMetrics.conversion_rate}%</div>
          <div className="text-xs text-gray-500">Overall Conversion</div>
        </div>
      </div>
    </div>
  );

  const ContentScheduler = () => (
    <div className="bg-white rounded-lg p-6 border border-gray-200 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold">Content Queue</h3>
        <button className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700">
          + Add Content
        </button>
      </div>
      
      <div className="space-y-3">
        {contentQueue.map((item, idx) => (
          <div key={idx} className="flex items-center justify-between p-3 border border-gray-100 rounded">
            <div className="flex items-center space-x-3">
              <div className={`w-3 h-3 rounded-full ${
                item.status === 'pending' ? 'bg-yellow-400' : 
                item.status === 'posted' ? 'bg-green-400' : 'bg-gray-400'
              }`}></div>
              <div>
                <div className="font-medium text-sm capitalize">{item.platform}</div>
                <div className="text-xs text-gray-500">{item.type.replace('_', ' ')}</div>
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm font-medium">{item.scheduled}</div>
              <div className={`text-xs capitalize ${
                item.status === 'pending' ? 'text-yellow-600' :
                item.status === 'posted' ? 'text-green-600' : 'text-gray-600'
              }`}>
                {item.status}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const BotDeploymentGuide = () => (
    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 border border-blue-200">
      <h3 className="font-bold text-lg mb-4 text-blue-900">🚀 One-Click Bot Deployment</h3>
      
      <div className="grid md:grid-cols-3 gap-4 mb-6">
        <div className="bg-white rounded-lg p-4 border border-blue-200">
          <div className="flex items-center space-x-2 mb-3">
            <MessageCircle className="w-5 h-5 text-indigo-600" />
            <h4 className="font-semibold">Discord Bot</h4>
          </div>
          <p className="text-sm text-gray-600 mb-3">Add live market analysis to any Discord server</p>
          <div className="space-y-2">
            <button className="w-full bg-indigo-600 text-white py-2 px-3 rounded text-sm hover:bg-indigo-700">
              Add to Discord
            </button>
            <button className="w-full border border-indigo-600 text-indigo-600 py-2 px-3 rounded text-sm hover:bg-indigo-50">
              Get Embed Code
            </button>
          </div>
        </div>
        
        <div className="bg-white rounded-lg p-4 border border-blue-200">
          <div className="flex items-center space-x-2 mb-3">
            <Send className="w-5 h-5 text-cyan-600" />
            <h4 className="font-semibold">Telegram Bot</h4>
          </div>
          <p className="text-sm text-gray-600 mb-3">Get market signals in Telegram channels</p>
          <div className="space-y-2">
            <button className="w-full bg-cyan-600 text-white py-2 px-3 rounded text-sm hover:bg-cyan-700">
              Add to Telegram
            </button>
            <button className="w-full border border-cyan-600 text-cyan-600 py-2 px-3 rounded text-sm hover:bg-cyan-50">
              Channel Setup
            </button>
          </div>
        </div>
        
        <div className="bg-white rounded-lg p-4 border border-blue-200">
          <div className="flex items-center space-x-2 mb-3">
            <Twitter className="w-5 h-5 text-blue-600" />
            <h4 className="font-semibold">Twitter Bot</h4>
          </div>
          <p className="text-sm text-gray-600 mb-3">Auto-tweet market updates and engage</p>
          <div className="space-y-2">
            <button className="w-full bg-blue-600 text-white py-2 px-3 rounded text-sm hover:bg-blue-700">
              Connect Twitter
            </button>
            <button className="w-full border border-blue-600 text-blue-600 py-2 px-3 rounded text-sm hover:bg-blue-50">
              Automation Rules
            </button>
          </div>
        </div>
      </div>
      
      <div className="bg-white rounded-lg p-4 border border-blue-200">
        <h4 className="font-semibold mb-3 flex items-center">
          <Zap className="w-5 h-5 mr-2 text-yellow-600" />
          Quick Setup Script
        </h4>
        <div className="bg-gray-900 text-gray-100 p-4 rounded text-sm font-mono overflow-x-auto">
          <div className="text-green-400"># One-command setup</div>
          <div className="text-blue-400">curl -sSL https://setup.marketgeometry.com/install.sh | bash</div>
          <div className="text-gray-400 mt-2"># Sets up all bots with your API keys</div>
          <div className="text-gray-400"># Configures webhooks and automation</div>
          <div className="text-gray-400"># Starts monitoring dashboard</div>
        </div>
        <button className="mt-3 bg-green-600 text-white px-4 py-2 rounded text-sm hover:bg-green-700">
          <Download className="w-4 h-4 inline mr-1" />
          Download Setup Script
        </button>
      </div>
    </div>
  );

  const ViralContentExamples = () => (
    <div className="grid md:grid-cols-2 gap-6">
      <div className="bg-white rounded-lg p-6 border border-gray-200 shadow-sm">
        <h3 className="font-semibold mb-4 flex items-center">
          <Twitter className="w-5 h-5 mr-2 text-blue-600" />
          Viral Twitter Templates
        </h3>
        
        <div className="space-y-4">
          {[
            {
              type: "FOMO Hook",
              content: "🚨 BREAKING: $AAPL showing the EXACT pattern that predicted Tesla's 340% run\n\nOur geometric AI just flagged critical confluence at 87.3%\n\nThis thread will be deleted in 2 hours... 🧵👇",
              engagement: "2.3K likes, 847 RTs"
            },
            {
              type: "Social Proof",
              content: "Update: 1,247 traders now using our 3D market analysis\n\nResults this month:\n📊 87% win rate\n💰 Avg gain: +11.3%\n🎯 Called $BTC bottom at $15,547\n\nThe geometry doesn't lie 📈\n\nTry free: [link]",
              engagement: "1.8K likes, 456 RTs"
            },
            {
              type: "Exclusive Alpha",
              content: "🤫 Whale alert: Someone just accumulated 2.3M shares of mystery tech stock\n\nOur pattern recognition flagged this 👀\n\nLike this tweet for the ticker\n\n(First 500 people only)",
              engagement: "4.1K likes, 1.2K RTs"
            }
          ].map((template, idx) => (
            <div key={idx} className="border border-gray-100 rounded p-3">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-1 rounded">
                  {template.type}
                </span>
                <span className="text-xs text-gray-500">{template.engagement}</span>
              </div>
              <p className="text-sm text-gray-800 mb-2">{template.content}</p>
              <button className="text-xs text-blue-600 hover:text-blue-800">Use Template →</button>
            </div>
          ))}
        </div>
      </div>
      
      <div className="bg-white rounded-lg p-6 border border-gray-200 shadow-sm">
        <h3 className="font-semibold mb-4 flex items-center">
          <Send className="w-5 h-5 mr-2 text-cyan-600" />
          Telegram Signal Templates
        </h3>
        
        <div className="space-y-4">
          {[
            {
              type: "Signal Alert",
              content: "🎯 SIGNAL ALERT\n\n📊 $TSLA\n💰 Entry: $242.50\n🔥 Target: $267.80 (+10.4%)\n⛔ Stop: $231.20 (-4.7%)\n\n🤖 AI Confidence: 87.3%\n📈 Geometric Pattern: Bullish Triangle\n⏰ Time Frame: 2-5 days",
              subscribers: "3,891 subscribers"
            },
            {
              type: "Market Update", 
              content: "📈 MARKET UPDATE\n\n🔥 Top Movers:\n• $AAPL +3.2% (confluence: 84%)\n• $MSFT +2.7% (confluence: 91%)\n• $GOOGL +1.8% (confluence: 76%)\n\n💡 Pattern: Tech rotation forming\n🎯 Opportunity: Long tech, short energy\n\n👆 Get full analysis",
              subscribers: "3,891 subscribers"
            },
            {
              type: "Exclusive Preview",
              content: "🔐 PREMIUM PREVIEW\n\n🐋 Whale movement detected:\n• 47M volume spike in mystery stock\n• Geometric indicators aligning\n• Institution accumulation pattern\n\n⚠️ Full details in premium channel\n⏰ Offer expires in 24h\n\n💎 Upgrade now: [link]",
              subscribers: "3,891 subscribers"
            }
          ].map((template, idx) => (
            <div key={idx} className="border border-gray-100 rounded p-3">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-medium text-cyan-600 bg-cyan-50 px-2 py-1 rounded">
                  {template.type}
                </span>
                <span className="text-xs text-gray-500">{template.subscribers}</span>
              </div>
              <div className="text-sm text-gray-800 mb-2 whitespace-pre-line font-mono bg-gray-50 p-2 rounded">
                {template.content}
              </div>
              <button className="text-xs text-cyan-600 hover:text-cyan-800">Use Template →</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const ROICalculator = () => (
    <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg p-6 border border-green-200">
      <h3 className="font-bold text-lg mb-4 text-green-900">💰 Social Media ROI Calculator</h3>
      
      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <h4 className="font-semibold mb-3">Current Performance</h4>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-sm">Total Reach:</span>
              <span className="font-bold">147,283</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm">Click-through Rate:</span>
              <span className="font-bold text-blue-600">4.2%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm">Conversion Rate:</span>
              <span className="font-bold text-green-600">2.8%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm">Average Order Value:</span>
              <span className="font-bold">$97</span>
            </div>
          </div>
        </div>
        
        <div>
          <h4 className="font-semibold mb-3">Projected Growth</h4>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-sm">Monthly Revenue:</span>
              <span className="font-bold text-green-600">$28,947</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm">Growth Rate:</span>
              <span className="font-bold text-purple-600">+23% MoM</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm">6-Month Projection:</span>
              <span className="font-bold text-green-600">$87,241</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm">Annual Projection:</span>
              <span className="font-bold text-green-600">$347,364</span>
            </div>
          </div>
        </div>
      </div>
      
      <div className="mt-6 p-4 bg-white rounded border border-green-200">
        <div className="flex items-center justify-between">
          <div>
            <div className="font-bold text-2xl text-green-600">$312,417</div>
            <div className="text-sm text-gray-600">Net profit (12 months)</div>
          </div>
          <div>
            <div className="font-bold text-2xl text-purple-600">847%</div>
            <div className="text-sm text-gray-600">ROI on social investment</div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            🚀 Viral Social Media Marketing Center
          </h1>
          <p className="text-gray-600">
            Automated bots, viral content, and conversion funnels for explosive growth
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="mb-8">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8">
              {[
                { id: 'overview', label: 'Overview', icon: BarChart3 },
                { id: 'bots', label: 'Social Bots', icon: Bot },
                { id: 'viral', label: 'Viral Strategies', icon: TrendingUp },
                { id: 'content', label: 'Content Templates', icon: MessageCircle },
                { id: 'deployment', label: 'Easy Deploy', icon: Zap }
              ].map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <tab.icon className="w-4 h-4 inline mr-2" />
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        {activeTab === 'overview' && (
          <div className="space-y-8">
            {/* Key Metrics */}
            <div className="grid md:grid-cols-4 gap-6">
              <div className="bg-white rounded-lg p-6 border border-gray-200 shadow-sm">
                <div className="flex items-center">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Eye className="w-6 h-6 text-blue-600" />
                  </div>
                  <div className="ml-4">
                    <div className="text-2xl font-bold text-gray-900">147K</div>
                    <div className="text-sm text-gray-500">Total Reach</div>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg p-6 border border-gray-200 shadow-sm">
                <div className="flex items-center">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <Users className="w-6 h-6 text-green-600" />
                  </div>
                  <div className="ml-4">
                    <div className="text-2xl font-bold text-gray-900">16.8K</div>
                    <div className="text-sm text-gray-500">Total Followers</div>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg p-6 border border-gray-200 shadow-sm">
                <div className="flex items-center">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <Target className="w-6 h-6 text-purple-600" />
                  </div>
                  <div className="ml-4">
                    <div className="text-2xl font-bold text-gray-900">2.8%</div>
                    <div className="text-sm text-gray-500">Conversion Rate</div>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg p-6 border border-gray-200 shadow-sm">
                <div className="flex items-center">
                  <div className="p-2 bg-yellow-100 rounded-lg">
                    <Crown className="w-6 h-6 text-yellow-600" />
                  </div>
                  <div className="ml-4">
                    <div className="text-2xl font-bold text-gray-900">$28.9K</div>
                    <div className="text-sm text-gray-500">Monthly Revenue</div>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="grid md:grid-cols-2 gap-6">
              <ConversionFunnelChart />
              <ContentScheduler />
            </div>
            
            <ROICalculator />
          </div>
        )}

        {activeTab === 'bots' && (
          <div className="space-y-8">
            <div className="grid md:grid-cols-3 gap-6">
              <AutomationCard
                platform="discord"
                icon={MessageCircle}
                metrics={botStatus.discord}
                status={botStatus.discord}
              />
              <AutomationCard
                platform="telegram"
                icon={Send}
                metrics={botStatus.telegram}
                status={botStatus.telegram}
              />
              <AutomationCard
                platform="twitter"
                icon={Twitter}
                metrics={botStatus.twitter}
                status={botStatus.twitter}
              />
            </div>
          </div>
        )}

        {activeTab === 'viral' && (
          <div className="space-y-8">
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {viralStrategies.map((strategy, idx) => (
                <ViralStrategyCard key={idx} strategy={strategy} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'content' && (
          <div className="space-y-8">
            <ViralContentExamples />
          </div>
        )}

        {activeTab === 'deployment' && (
          <div className="space-y-8">
            <BotDeploymentGuide />
          </div>
        )}
      </div>
    </div>
  );
};

export default ViralMarketingDashboard;flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className={`p-2 rounded-lg ${
            platform === 'discord' ? 'bg-indigo-100' :
            platform === 'twitter' ? 'bg-blue-100' : 'bg-cyan-100'
          }`}>
            <Icon className={`w-6 h-6 ${
              platform === 'discord' ? 'text-indigo-600' :
              platform === 'twitter' ? 'text-blue-600' : 'text-cyan-600'
            }`} />
          </div>
          <h3 className="font-semibold capitalize">{platform}</h3>
        </div>
        <div className={`px-2 py-1 rounded-full text-xs ${
          status.active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
        }`}>
          {status.active ? 'Active' : 'Inactive'}
        </div>
      </div>
      
      <div className="space-y-3">
        {Object.entries(metrics).map(([key, value], index) => (
          <div key={index} className="flex justify-between items-center">
            <span className="text-sm text-gray-600 capitalize">{key.replace('_', ' ')}</span>
            <span className="font-medium">{typeof value === 'number' ? value.toLocaleString() : value}</span>
          </div>
        ))}
      </div>
      
      <div className="mt-4 flex space-x-2">
        <button className="flex-1 bg-gray-100 text-gray-700 px-3 py-2 rounded text-sm hover:bg-gray-200">
          <Settings className="w-4 h-4 inline mr-1" />
          Configure
        </button>
        <button className={`flex-1 px-3 py-2 rounded text-sm text-white ${
          status.active ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600'
        }`}>
          {status.active ? <Pause className="w-4 h-4 inline mr-1" /> : <Play className="w-4 h-4 inline mr-1" />}
          {status.active ? 'Pause' : 'Start'}
        </button>
      </div>
    </div>
  );

  const ViralStrategyCard = ({ strategy }) => (
    <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg p-6 border border-purple-200">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-purple-900">{strategy.name}</h3>
        <div className="flex items-center space-x-2">
          <span className="text-2xl font-bold text-purple-600">{strategy.conversion_rate}</span>
          <div className={`w-3 h-3 rounded-full ${
            strategy.status === 'active' ? 'bg-green-400' : 'bg-gray-400'
          }`}></div>
        </div>
      </div>
      
      <p className="text-sm text-gray-600 mb-4">{strategy.description}</p>
      
      <div className="mb-4">
        <div className="flex flex-wrap gap-2">
          {strategy.platforms.map((platform, idx) => (
            <span key={idx} className="px-2 py-1 bg-white rounded text-xs text-purple-700 border border-purple-200">
              {platform}
            </span>
          ))}
        </div>
      </div>
      
      <div className="space-y-2">
        <h4 className="text-xs font-medium text-gray-700 uppercase tracking-wide">Example Hooks:</h4>
        {strategy.examples.slice(0, 2).map((example, idx) => (
          <div key={idx} className="text-xs text-gray-600 bg-white p-2 rounded border border-purple-100">
            {example}
          </div>
        ))}
      </div>
      
      <button className="w-full mt-4 bg-purple-600 text-white py-2 rounded text-sm hover:bg-purple-700">
        Deploy Strategy
      </button>
    </div>
  );

  const ConversionFunnelChart = () => (
    <div className="bg-white rounded-lg p-6 border border-gray-200 shadow-sm">
      <h3 className="font-semibold mb-4">Conversion Funnel Performance</h3>
      
      <div className="space-y-4">
        {[
          { stage: 'Social Media Impression', count: 147283, rate: 100, color: 'bg-blue-500' },
          { stage: 'Click to Website', count: 6186, rate: 4.2, color: 'bg-green-500' },
          { stage: 'Demo Interaction', count: 2474, rate: 1.7, color: 'bg-yellow-500' },
          { stage: 'Trial Signup', count: 1238, rate: 0.8, color: 'bg-orange-500' },
          { stage: 'Paid Conversion', count: 412, rate: 0.3, color: 'bg-red-500' }
        ].map((stage, idx) => (
          <div key={idx} className="relative">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium">{stage.stage}</span>
              <div className="flex items-center space-x-3">
                <span className="text-sm text-gray-500">{stage.rate}%</span>
                <span className="font-bold">{stage.count.toLocaleString()}</span>
              </div>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div 
                className={`h-3 rounded-full ${stage.color}`}
                style={{ width: `${Math.max(stage.rate * 20, 5)}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
      
      <div className="
