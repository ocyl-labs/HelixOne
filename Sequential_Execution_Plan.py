import React, { useState, useEffect } from 'react';
import { 
  Play, 
  CheckCircle, 
  Clock, 
  AlertTriangle, 
  Code, 
  Database, 
  Cloud, 
  CreditCard, 
  Smartphone, 
  Shield,
  Users,
  TrendingUp,
  Zap,
  ArrowRight,
  GitBranch,
  Server,
  Bot
} from 'lucide-react';

const SequentialExecutionManager = () => {
  const [currentSprint, setCurrentSprint] = useState(0);
  const [sprintProgress, setSprintProgress] = useState({});
  const [isExecuting, setIsExecuting] = useState(false);
  const [completedSprints, setCompletedSprints] = useState(new Set());

  // Complete sprint execution plan
  const executionSprints = [
    {
      id: 'sprint-1',
      name: 'Production Backend API',
      duration: '2 weeks',
      priority: 'CRITICAL',
      icon: <Server className="w-6 h-6" />,
      description: 'Complete production-ready backend API with all endpoints',
      blockers: [],
      deliverables: [
        'FastAPI server with all market data endpoints',
        'PostgreSQL database with complete schema',
        'Redis caching layer for real-time data',
        'WebSocket server for live updates',
        'Authentication middleware with JWT',
        'Error handling and logging system'
      ],
      tasks: [
        {
          id: 'backend-setup',
          name: 'FastAPI Server Setup',
          estimate: '2 days',
          code_type: 'backend_api'
        },
        {
          id: 'database-implementation',
          name: 'PostgreSQL Implementation',
          estimate: '2 days', 
          code_type: 'database_schema'
        },
        {
          id: 'websocket-server',
          name: 'WebSocket Real-time Server',
          estimate: '2 days',
          code_type: 'websocket_server'
        },
        {
          id: 'auth-system',
          name: 'Authentication System',
          estimate: '2 days',
          code_type: 'auth_middleware'
        },
        {
          id: 'redis-caching',
          name: 'Redis Caching Layer',
          estimate: '1 day',
          code_type: 'redis_cache'
        },
        {
          id: 'api-testing',
          name: 'API Testing & Documentation',
          estimate: '1 day',
          code_type: 'api_tests'
        }
      ]
    },
    {
      id: 'sprint-2', 
      name: 'Live Market Data Integration',
      duration: '1.5 weeks',
      priority: 'CRITICAL',
      icon: <TrendingUp className="w-6 h-6" />,
      description: 'Real-time market data with multiple sources and failover',
      blockers: ['sprint-1'],
      deliverables: [
        'Yahoo Finance API integration with rate limiting',
        'CoinGecko API with error handling',
        'Alpha Vantage backup integration',
        'NewsAPI sentiment pipeline',
        'Data validation and cleansing',
        'Automatic failover between sources'
      ],
      tasks: [
        {
          id: 'yahoo-finance',
          name: 'Yahoo Finance Integration',
          estimate: '2 days',
          code_type: 'yahoo_finance_api'
        },
        {
          id: 'coingecko-api',
          name: 'CoinGecko Integration',
          estimate: '1 day',
          code_type: 'coingecko_api'
        },
        {
          id: 'alpha-vantage',
          name: 'Alpha Vantage Backup',
          estimate: '1 day',
          code_type: 'alpha_vantage_api'
        },
        {
          id: 'news-sentiment',
          name: 'News Sentiment Pipeline',
          estimate: '2 days',
          code_type: 'sentiment_pipeline'
        },
        {
          id: 'data-validation',
          name: 'Data Validation System',
          estimate: '1 day',
          code_type: 'data_validation'
        },
        {
          id: 'failover-system',
          name: 'Failover & Redundancy',
          estimate: '1 day',
          code_type: 'failover_system'
        }
      ]
    },
    {
      id: 'sprint-3',
      name: 'Payment & Subscription System',
      duration: '2 weeks', 
      priority: 'CRITICAL',
      icon: <CreditCard className="w-6 h-6" />,
      description: 'Complete payment processing with Stripe integration',
      blockers: ['sprint-1'],
      deliverables: [
        'Stripe payment integration with webhooks',
        'Subscription tier management system',
        'Payment failure handling and retry logic',
        'Invoice generation and tax calculation',
        'Refund processing workflow',
        'PCI compliance implementation'
      ],
      tasks: [
        {
          id: 'stripe-integration',
          name: 'Stripe Payment Integration',
          estimate: '3 days',
          code_type: 'stripe_integration'
        },
        {
          id: 'subscription-tiers',
          name: 'Subscription Management',
          estimate: '2 days',
          code_type: 'subscription_system'
        },
        {
          id: 'webhook-handling',
          name: 'Webhook Processing',
          estimate: '2 days',
          code_type: 'webhook_handlers'
        },
        {
          id: 'billing-system',
          name: 'Billing & Invoice System',
          estimate: '2 days',
          code_type: 'billing_system'
        },
        {
          id: 'payment-security',
          name: 'Security & Compliance',
          estimate: '1 day',
          code_type: 'payment_security'
        }
      ]
    },
    {
      id: 'sprint-4',
      name: 'Production Deployment',
      duration: '1.5 weeks',
      priority: 'CRITICAL', 
      icon: <Cloud className="w-6 h-6" />,
      description: 'Full production deployment with scaling and monitoring',
      blockers: ['sprint-1', 'sprint-2', 'sprint-3'],
      deliverables: [
        'AWS/Google Cloud production environment',
        'Docker containerization with Kubernetes',
        'Load balancing and auto-scaling',
        'SSL certificates and CDN setup',
        'Monitoring and alerting system',
        'Backup and disaster recovery'
      ],
      tasks: [
        {
          id: 'cloud-setup',
          name: 'Cloud Infrastructure Setup',
          estimate: '2 days',
          code_type: 'cloud_infrastructure'
        },
        {
          id: 'containerization',
          name: 'Docker & Kubernetes',
          estimate: '2 days',
          code_type: 'docker_kubernetes'
        },
        {
          id: 'load-balancing',
          name: 'Load Balancer & CDN',
          estimate: '1 day',
          code_type: 'load_balancer'
        },
        {
          id: 'monitoring-setup',
          name: 'Monitoring & Alerts',
          estimate: '2 days',
          code_type: 'monitoring_system'
        },
        {
          id: 'backup-system',
          name: 'Backup & Recovery',
          estimate: '1 day',
          code_type: 'backup_system'
        }
      ]
    },
    {
      id: 'sprint-5',
      name: 'User Authentication & Management',
      duration: '1 week',
      priority: 'HIGH',
      icon: <Shield className="w-6 h-6" />,
      description: 'Complete user management with OAuth and admin features',
      blockers: ['sprint-1'],
      deliverables: [
        'User registration and login system',
        'Email verification workflow',
        'OAuth integration (Google, Apple, Facebook)',
        'Password reset functionality',
        'User profile management',
        'Admin dashboard for user management'
      ],
      tasks: [
        {
          id: 'user-auth',
          name: 'User Authentication System',
          estimate: '2 days',
          code_type: 'user_auth_system'
        },
        {
          id: 'oauth-integration',
          name: 'OAuth Integration',
          estimate: '2 days',
          code_type: 'oauth_system'
        },
        {
          id: 'user-profiles',
          name: 'User Profile Management',
          estimate: '1 day',
          code_type: 'profile_management'
        },
        {
          id: 'admin-dashboard',
          name: 'Admin Dashboard',
          estimate: '2 days',
          code_type: 'admin_dashboard'
        }
      ]
    },
    {
      id: 'sprint-6',
      name: 'Social Media Bot Deployment',
      duration: '2 weeks',
      priority: 'HIGH',
      icon: <Bot className="w-6 h-6" />,
      description: 'Deploy and activate all social media bots with analytics',
      blockers: ['sprint-1', 'sprint-2'],
      deliverables: [
        'Discord bot hosting with slash commands',
        'Telegram bot with webhook integration',
        'Twitter automation with posting schedule',
        'Content generation AI system',
        'Social analytics and tracking',
        'Compliance monitoring system'
      ],
      tasks: [
        {
          id: 'discord-bot-deploy',
          name: 'Discord Bot Deployment',
          estimate: '2 days',
          code_type: 'discord_bot_deploy'
        },
        {
          id: 'telegram-bot-deploy',
          name: 'Telegram Bot Deployment',
          estimate: '2 days',
          code_type: 'telegram_bot_deploy'
        },
        {
          id: 'twitter-automation',
          name: 'Twitter Automation',
          estimate: '2 days',
          code_type: 'twitter_automation'
        },
        {
          id: 'content-generation',
          name: 'AI Content Generation',
          estimate: '3 days',
          code_type: 'content_ai_system'
        },
        {
          id: 'social-analytics',
          name: 'Social Media Analytics',
          estimate: '2 days',
          code_type: 'social_analytics'
        },
        {
          id: 'compliance-monitoring',
          name: 'Compliance & Moderation',
          estimate: '1 day',
          code_type: 'compliance_system'
        }
      ]
    },
    {
      id: 'sprint-7',
      name: 'Legal Compliance Integration',
      duration: '1 week',
      priority: 'HIGH',
      icon: <AlertTriangle className="w-6 h-6" />,
      description: 'Complete legal framework integration throughout platform',
      blockers: ['sprint-1', 'sprint-5'],
      deliverables: [
        'Terms of Service integration in app',
        'Privacy Policy with GDPR compliance',
        'Cookie consent management system',
        'Financial disclaimers throughout',
        'Data export and deletion tools',
        'Audit logging system'
      ],
      tasks: [
        {
          id: 'legal-integration',
          name: 'Legal Document Integration',
          estimate: '2 days',
          code_type: 'legal_integration'
        },
        {
          id: 'gdpr-system',
          name: 'GDPR Compliance System',
          estimate: '2 days',
          code_type: 'gdpr_compliance'
        },
        {
          id: 'consent-management',
          name: 'Consent Management',
          estimate: '1 day',
          code_type: 'consent_system'
        },
        {
          id: 'audit-logging',
          name: 'Audit & Logging System',
          estimate: '2 days',
          code_type: 'audit_system'
        }
      ]
    },
    {
      id: 'sprint-8',
      name: 'Advanced AI/ML Features',
      duration: '3 weeks',
      priority: 'MEDIUM',
      icon: <Zap className="w-6 h-6" />,
      description: 'Advanced predictive analytics and machine learning',
      blockers: ['sprint-2'],
      deliverables: [
        'LSTM price prediction models',
        'Advanced sentiment analysis',
        'Portfolio optimization algorithms',
        'Risk management calculations',
        'Pattern recognition ML',
        'Backtesting engine'
      ],
      tasks: [
        {
          id: 'lstm-models',
          name: 'LSTM Price Prediction',
          estimate: '5 days',
          code_type: 'lstm_prediction'
        },
        {
          id: 'advanced-sentiment',
          name: 'Advanced Sentiment Analysis',
          estimate: '3 days',
          code_type: 'advanced_sentiment'
        },
        {
          id: 'portfolio-optimization',
          name: 'Portfolio Optimization',
          estimate: '4 days',
          code_type: 'portfolio_optimizer'
        },
        {
          id: 'risk-management',
          name: 'Risk Management System',
          estimate: '3 days',
          code_type: 'risk_management'
        },
        {
          id: 'pattern-recognition',
          name: 'Pattern Recognition ML',
          estimate: '4 days',
          code_type: 'pattern_recognition'
        },
        {
          id: 'backtesting-engine',
          name: 'Backtesting Engine',
          estimate: '2 days',
          code_type: 'backtesting_system'
        }
      ]
    }
  ];

  const SprintCard = ({ sprint, index, isActive, isCompleted, isBlocked }) => {
    const canStart = sprint.blockers.every(blocker => 
      executionSprints.find(s => s.id === blocker) ? completedSprints.has(blocker) : true
    );

    return (
      <div className={`border rounded-lg p-6 transition-all ${
        isCompleted ? 'bg-green-50 border-green-200' :
        isActive ? 'bg-blue-50 border-blue-300 shadow-lg' :
        isBlocked || !canStart ? 'bg-gray-50 border-gray-200 opacity-60' :
        'bg-white border-gray-200 hover:border-blue-200'
      }`}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className={`p-2 rounded-lg ${
              isCompleted ? 'bg-green-100' :
              isActive ? 'bg-blue-100' : 'bg-gray-100'
            }`}>
              {isCompleted ? (
                <CheckCircle className="w-6 h-6 text-green-600" />
              ) : (
                sprint.icon
              )}
            </div>
            <div>
              <h3 className="font-bold text-lg">{sprint.name}</h3>
              <div className="flex items-center space-x-4 text-sm">
                <span className="text-gray-600">{sprint.duration}</span>
                <span className={`px-2 py-1 rounded text-xs font-medium ${
                  sprint.priority === 'CRITICAL' ? 'bg-red-100 text-red-700' :
                  sprint.priority === 'HIGH' ? 'bg-orange-100 text-orange-700' :
                  'bg-blue-100 text-blue-700'
                }`}>
                  {sprint.priority}
                </span>
              </div>
            </div>
          </div>
          
          <div className="text-right">
            <div className="text-xl font-bold text-gray-600">
              Sprint {index + 1}
            </div>
            {canStart && !isCompleted && !isActive && (
              <button
                onClick={() => executeSprint(sprint.id)}
                className="mt-2 bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700"
              >
                <Play className="w-4 h-4 inline mr-1" />
                Execute
              </button>
            )}
          </div>
        </div>

        <p className="text-gray-600 mb-4">{sprint.description}</p>

        {sprint.blockers.length > 0 && (
          <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded">
            <div className="flex items-center text-sm text-yellow-700">
              <AlertTriangle className="w-4 h-4 mr-2" />
              Blocked by: {sprint.blockers.join(', ')}
            </div>
          </div>
        )}

        <div className="mb-4">
          <h4 className="font-semibold text-sm mb-2">Key Deliverables:</h4>
          <div className="grid grid-cols-1 gap-1">
            {sprint.deliverables.slice(0, 3).map((deliverable, idx) => (
              <div key={idx} className="text-sm text-gray-600 flex items-center">
                <CheckCircle className="w-3 h-3 mr-2 text-green-500" />
                {deliverable}
              </div>
            ))}
            {sprint.deliverables.length > 3 && (
              <div className="text-xs text-gray-500">
                +{sprint.deliverables.length - 3} more deliverables
              </div>
            )}
          </div>
        </div>

        <div className="space-y-2">
          <h4 className="font-semibold text-sm">Tasks ({sprint.tasks.length}):</h4>
          <div className="space-y-1">
            {sprint.tasks.map((task, idx) => (
              <div key={idx} className="flex items-center justify-between text-sm">
                <span className="text-gray-600">{task.name}</span>
                <span className="text-xs text-gray-500">{task.estimate}</span>
              </div>
            ))}
          </div>
        </div>

        {isActive && (
          <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-blue-700">Sprint Progress</span>
              <span className="text-sm text-blue-600">
                {Math.round((sprintProgress[sprint.id] || 0))}%
              </span>
            </div>
            <div className="w-full bg-blue-200 rounded-full h-2">
              <div 
                className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                style={{ width: `${sprintProgress[sprint.id] || 0}%` }}
              ></div>
            </div>
          </div>
        )}
      </div>
    );
  };

  const executeSprint = async (sprintId) => {
    const sprint = executionSprints.find(s => s.id === sprintId);
    if (!sprint) return;

    setCurrentSprint(executionSprints.indexOf(sprint));
    setIsExecuting(true);

    // Simulate sprint execution with progress updates
    for (let progress = 0; progress <= 100; progress += 5) {
      setSprintProgress(prev => ({ ...prev, [sprintId]: progress }));
      await new Promise(resolve => setTimeout(resolve, 200));
    }

    setCompletedSprints(prev => new Set([...prev, sprintId]));
    setIsExecuting(false);

    // Auto-start next sprint if dependencies are met
    const nextSprintIndex = executionSprints.indexOf(sprint) + 1;
    if (nextSprintIndex < executionSprints.length) {
      const nextSprint = executionSprints[nextSprintIndex];
      const canStartNext = nextSprint.blockers.every(blocker => 
        completedSprints.has(blocker) || blocker === sprintId
      );
      
      if (canStartNext) {
        setTimeout(() => executeSprint(nextSprint.id), 1000);
      }
    }
  };

  const executeAllSprints = async () => {
    setIsExecuting(true);
    
    for (const sprint of executionSprints) {
      // Check if dependencies are met
      const canStart = sprint.blockers.every(blocker => 
        completedSprints.has(blocker)
      );
      
      if (canStart && !completedSprints.has(sprint.id)) {
        await executeSprint(sprint.id);
        await new Promise(resolve => setTimeout(resolve, 500));
      }
    }
    
    setIsExecuting(false);
  };

  const overallProgress = () => {
    return (completedSprints.size / executionSprints.length) * 100;
  };

  const getTotalTime = () => {
    return executionSprints.reduce((total, sprint) => {
      const weeks = parseFloat(sprint.duration.split(' ')[0]);
      return total + weeks;
    }, 0);
  };

  const getTotalCost = () => {
    const hourlyRate = 150;
    const totalHours = executionSprints.reduce((total, sprint) => {
      return total + sprint.tasks.reduce((taskTotal, task) => {
        const days = parseFloat(task.estimate.split(' ')[0]);
        return taskTotal + (days * 8); // 8 hours per day
      }, 0);
    }, 0);
    
    return totalHours * hourlyRate;
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            🚀 HelixOne Sequential Execution Plan
          </h1>
          <p className="text-gray-600">
            Complete sprint-by-sprint implementation to 100% turnkey ready
          </p>
        </div>

        {/* Overall Progress */}
        <div className="bg-white rounded-xl p-6 mb-8 shadow-sm border border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Overall Progress</h3>
              <div className="text-3xl font-bold text-blue-600">
                {Math.round(overallProgress())}%
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3 mt-2">
                <div 
                  className="bg-blue-500 h-3 rounded-full transition-all duration-500"
                  style={{ width: `${overallProgress()}%` }}
                ></div>
              </div>
            </div>
            
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Total Timeline</h3>
              <div className="text-3xl font-bold text-green-600">
                {getTotalTime()} weeks
              </div>
              <div className="text-sm text-gray-500 mt-2">Sequential execution</div>
            </div>
            
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Total Investment</h3>
              <div className="text-3xl font-bold text-purple-600">
                ${getTotalCost().toLocaleString()}
              </div>
              <div className="text-sm text-gray-500 mt-2">Development cost</div>
            </div>

            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Sprints Complete</h3>
              <div className="text-3xl font-bold text-orange-600">
                {completedSprints.size}/{executionSprints.length}
              </div>
              <button
                onClick={executeAllSprints}
                disabled={isExecuting}
                className="mt-2 bg-orange-600 text-white px-4 py-2 rounded text-sm hover:bg-orange-700 disabled:opacity-50"
              >
                Execute All Sprints
              </button>
            </div>
          </div>
        </div>

        {/* Sprint Cards */}
        <div className="space-y-6">
          {executionSprints.map((sprint, index) => {
            const isActive = currentSprint === index && isExecuting;
            const isCompleted = completedSprints.has(sprint.id);
            const isBlocked = sprint.blockers.some(blocker => !completedSprints.has(blocker));
            
            return (
              <SprintCard
                key={sprint.id}
                sprint={sprint}
                index={index}
                isActive={isActive}
                isCompleted={isCompleted}
                isBlocked={isBlocked}
              />
            );
          })}
        </div>

        {/* Success Message */}
        {completedSprints.size === executionSprints.length && (
          <div className="mt-8 bg-green-50 border border-green-200 rounded-lg p-6">
            <div className="flex items-center">
              <CheckCircle className="w-8 h-8 text-green-600 mr-3" />
              <div>
                <h3 className="text-lg font-bold text-green-900">
                  🎉 HelixOne Market Intelligence is 100% Complete!
                </h3>
                <p className="text-green-700">
                  All sprints executed successfully. Your platform is now turnkey ready for launch!
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SequentialExecutionManager;
