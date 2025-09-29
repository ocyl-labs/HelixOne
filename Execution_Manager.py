import React, { useState, useEffect } from 'react';
import { CheckCircle, Circle, Clock, AlertCircle, Play, Pause, Code, Database, Smartphone, Shield, Gavel, Settings, TrendingUp, Users, Brain, Eye } from 'lucide-react';

const ProjectExecutionManager = () => {
  const [currentPhase, setCurrentPhase] = useState(0);
  const [activeTasks, setActiveTasks] = useState(new Set());
  const [completedTasks, setCompletedTasks] = useState(new Set());
  const [taskProgress, setTaskProgress] = useState({});
  const [isExecuting, setIsExecuting] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);
  const [generatedCode, setGeneratedCode] = useState('');

  // Complete project roadmap with all tasks
  const projectPhases = [
    {
      id: 'infrastructure',
      name: 'Infrastructure & Backend',
      duration: '3 weeks',
      cost: '$15,000',
      priority: 'Critical',
      icon: <Database className="w-6 h-6" />,
      description: 'Core backend infrastructure and production deployment',
      tasks: [
        {
          id: 'cloud-setup',
          name: 'Cloud Infrastructure Setup',
          duration: '3 days',
          dependencies: [],
          description: 'AWS/GCP setup with auto-scaling, load balancers, and CDN',
          deliverables: ['Production servers', 'Load balancer config', 'CDN setup'],
          codeTemplate: 'infrastructure-terraform'
        },
        {
          id: 'database-design',
          name: 'Database Architecture',
          duration: '2 days',
          dependencies: ['cloud-setup'],
          description: 'PostgreSQL setup with user data, market data, and analytics schemas',
          deliverables: ['Database schema', 'Migration scripts', 'Backup system'],
          codeTemplate: 'database-schema'
        },
        {
          id: 'api-gateway',
          name: 'API Gateway & Authentication',
          duration: '4 days',
          dependencies: ['database-design'],
          description: 'Secure API endpoints with JWT auth and rate limiting',
          deliverables: ['API gateway', 'Auth system', 'Rate limiting'],
          codeTemplate: 'api-gateway'
        },
        {
          id: 'data-pipeline',
          name: 'Real-time Data Pipeline',
          duration: '3 days',
          dependencies: ['api-gateway'],
          description: 'Enhanced market data ingestion with redundancy',
          deliverables: ['Data pipeline', 'Failover system', 'Data validation'],
          codeTemplate: 'data-pipeline'
        },
        {
          id: 'caching-layer',
          name: 'Redis Caching System',
          duration: '2 days',
          dependencies: ['data-pipeline'],
          description: 'High-performance caching for real-time data',
          deliverables: ['Redis cluster', 'Cache strategies', 'Performance optimization'],
          codeTemplate: 'redis-cache'
        }
      ]
    },
    {
      id: 'saas-platform',
      name: 'SaaS Platform',
      duration: '5 weeks',
      cost: '$20,000',
      priority: 'Critical',
      icon: <TrendingUp className="w-6 h-6" />,
      description: 'Complete SaaS infrastructure with payments and user management',
      tasks: [
        {
          id: 'user-management',
          name: 'User Management System',
          duration: '5 days',
          dependencies: ['api-gateway'],
          description: 'Registration, profiles, preferences, and admin dashboard',
          deliverables: ['User system', 'Admin panel', 'Profile management'],
          codeTemplate: 'user-management'
        },
        {
          id: 'payment-system',
          name: 'Payment Processing',
          duration: '4 days',
          dependencies: ['user-management'],
          description: 'Stripe integration with subscription management',
          deliverables: ['Payment gateway', 'Subscription tiers', 'Billing system'],
          codeTemplate: 'payment-system'
        },
        {
          id: 'subscription-management',
          name: 'Subscription Tiers',
          duration: '3 days',
          dependencies: ['payment-system'],
          description: 'Feature gating and tier management',
          deliverables: ['Tier system', 'Feature gates', 'Usage tracking'],
          codeTemplate: 'subscription-tiers'
        },
        {
          id: 'analytics-dashboard',
          name: 'Business Analytics',
          duration: '4 days',
          dependencies: ['subscription-management'],
          description: 'Revenue tracking and user behavior analytics',
          deliverables: ['Analytics system', 'Revenue reports', 'User insights'],
          codeTemplate: 'business-analytics'
        }
      ]
    },
    {
      id: 'mobile-apps',
      name: 'Mobile Applications',
      duration: '8 weeks',
      cost: '$75,000',
      priority: 'High',
      icon: <Smartphone className="w-6 h-6" />,
      description: 'Native iOS and Android applications',
      tasks: [
        {
          id: 'mobile-architecture',
          name: 'Mobile App Architecture',
          duration: '3 days',
          dependencies: ['api-gateway'],
          description: 'React Native setup with navigation and state management',
          deliverables: ['App structure', 'Navigation system', 'State management'],
          codeTemplate: 'mobile-architecture'
        },
        {
          id: 'mobile-3d-engine',
          name: 'Mobile 3D Rendering',
          duration: '7 days',
          dependencies: ['mobile-architecture'],
          description: 'Optimized 3D visualization for mobile devices',
          deliverables: ['3D renderer', 'Touch controls', 'Performance optimization'],
          codeTemplate: 'mobile-3d'
        },
        {
          id: 'ios-specific',
          name: 'iOS Implementation',
          duration: '10 days',
          dependencies: ['mobile-3d-engine'],
          description: 'iOS-specific features and App Store compliance',
          deliverables: ['iOS app', 'TestFlight setup', 'App Store listing'],
          codeTemplate: 'ios-app'
        },
        {
          id: 'android-specific',
          name: 'Android Implementation',
          duration: '10 days',
          dependencies: ['mobile-3d-engine'],
          description: 'Android-specific features and Google Play compliance',
          deliverables: ['Android app', 'Play Console setup', 'Store listing'],
          codeTemplate: 'android-app'
        }
      ]
    },
    {
      id: 'legal-compliance',
      name: 'Legal Framework',
      duration: '3 weeks',
      cost: '$12,000',
      priority: 'Critical',
      icon: <Gavel className="w-6 h-6" />,
      description: 'Legal compliance and regulatory framework',
      tasks: [
        {
          id: 'legal-docs',
          name: 'Legal Documentation',
          duration: '4 days',
          dependencies: [],
          description: 'Terms of Service, Privacy Policy, and compliance docs',
          deliverables: ['TOS', 'Privacy Policy', 'Data agreements'],
          codeTemplate: 'legal-docs'
        },
        {
          id: 'gdpr-compliance',
          name: 'GDPR/CCPA Compliance',
          duration: '3 days',
          dependencies: ['legal-docs'],
          description: 'Data protection and privacy compliance',
          deliverables: ['GDPR system', 'Consent management', 'Data export'],
          codeTemplate: 'gdpr-system'
        },
        {
          id: 'financial-compliance',
          name: 'Financial Regulations',
          duration: '5 days',
          dependencies: ['gdpr-compliance'],
          description: 'SEC compliance and financial disclaimers',
          deliverables: ['Risk disclaimers', 'Compliance monitoring', 'Audit system'],
          codeTemplate: 'financial-compliance'
        }
      ]
    },
    {
      id: 'ai-enhancements',
      name: 'AI/ML Features',
      duration: '6 weeks',
      cost: '$30,000',
      priority: 'High',
      icon: <Brain className="w-6 h-6" />,
      description: 'Advanced AI-powered predictive analytics',
      tasks: [
        {
          id: 'predictive-engine',
          name: 'Price Prediction System',
          duration: '8 days',
          dependencies: ['data-pipeline'],
          description: 'LSTM-based price prediction with confidence scoring',
          deliverables: ['ML models', 'Prediction API', 'Confidence metrics'],
          codeTemplate: 'predictive-ai'
        },
        {
          id: 'sentiment-analysis',
          name: 'Advanced Sentiment Analysis',
          duration: '5 days',
          dependencies: ['predictive-engine'],
          description: 'Multi-source sentiment with social media integration',
          deliverables: ['Sentiment engine', 'Social feeds', 'News analysis'],
          codeTemplate: 'sentiment-ai'
        },
        {
          id: 'risk-management',
          name: 'AI Risk Assessment',
          duration: '6 days',
          dependencies: ['sentiment-analysis'],
          description: 'Portfolio risk analysis with VaR calculations',
          deliverables: ['Risk engine', 'VaR calculations', 'Risk alerts'],
          codeTemplate: 'risk-ai'
        }
      ]
    },
    {
      id: 'advanced-features',
      name: 'Advanced Features',
      duration: '8 weeks',
      cost: '$40,000',
      priority: 'Medium',
      icon: <Eye className="w-6 h-6" />,
      description: 'Premium features for competitive advantage',
      tasks: [
        {
          id: 'social-trading',
          name: 'Social Trading Platform',
          duration: '10 days',
          dependencies: ['user-management'],
          description: 'Copy trading and community features',
          deliverables: ['Social system', 'Copy trading', 'Leaderboards'],
          codeTemplate: 'social-trading'
        },
        {
          id: 'portfolio-optimizer',
          name: 'Portfolio Optimization',
          duration: '7 days',
          dependencies: ['risk-management'],
          description: 'Modern Portfolio Theory implementation',
          deliverables: ['Optimizer engine', 'Allocation tools', 'Rebalancing'],
          codeTemplate: 'portfolio-optimizer'
        },
        {
          id: 'algorithmic-trading',
          name: 'Algo Trading Integration',
          duration: '12 days',
          dependencies: ['portfolio-optimizer'],
          description: 'Broker integration for automated trading',
          deliverables: ['Trading API', 'Strategy builder', 'Backtesting'],
          codeTemplate: 'algo-trading'
        }
      ]
    }
  ];

  const codeTemplates = {
    'infrastructure-terraform': `# Infrastructure as Code - Terraform
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC Configuration
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "financial-market-vpc"
    Environment = var.environment
  }
}

# Auto Scaling Group for Application Servers
resource "aws_autoscaling_group" "app" {
  name                = "financial-market-asg"
  vpc_zone_identifier = aws_subnet.private[*].id
  target_group_arns   = [aws_lb_target_group.app.arn]
  health_check_type   = "ELB"
  
  min_size         = 2
  max_size         = 20
  desired_capacity = 3
  
  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }
  
  tag {
    key                 = "Name"
    value               = "financial-market-server"
    propagate_at_launch = true
  }
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "financial-market-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets           = aws_subnet.public[*].id
  
  enable_deletion_protection = false
  
  tags = {
    Environment = var.environment
  }
}

# CloudFront Distribution for CDN
resource "aws_cloudfront_distribution" "main" {
  origin {
    domain_name = aws_lb.main.dns_name
    origin_id   = "ALB-${aws_lb.main.name}"
    
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }
  
  enabled = true
  
  default_cache_behavior {
    allowed_methods        = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "ALB-${aws_lb.main.name}"
    compress               = true
    viewer_protocol_policy = "redirect-to-https"
    
    forwarded_values {
      query_string = true
      headers      = ["Authorization", "CloudFront-Forwarded-Proto"]
      
      cookies {
        forward = "none"
      }
    }
    
    min_ttl     = 0
    default_ttl = 3600
    max_ttl     = 86400
  }
  
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
  
  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}`,

    'database-schema': `-- Financial Market Database Schema
-- PostgreSQL Implementation

-- Users and Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    subscription_tier VARCHAR(50) DEFAULT 'basic',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    last_login TIMESTAMP,
    preferences JSONB DEFAULT '{}'::jsonb
);

-- User Sessions for JWT Management
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    device_info JSONB,
    ip_address INET
);

-- Market Data Storage
CREATE TABLE market_assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol VARCHAR(50) NOT NULL,
    asset_type VARCHAR(50) NOT NULL, -- stocks, crypto, fx, etc.
    name VARCHAR(255),
    exchange VARCHAR(100),
    currency VARCHAR(10) DEFAULT 'USD',
    is_active BOOLEAN DEFAULT true,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_market_assets_symbol ON market_assets(symbol);
CREATE INDEX idx_market_assets_type ON market_assets(asset_type);

-- Real-time Market Data
CREATE TABLE market_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID REFERENCES market_assets(id),
    timestamp TIMESTAMP NOT NULL,
    price DECIMAL(15,8),
    volume DECIMAL(20,8),
    high DECIMAL(15,8),
    low DECIMAL(15,8),
    open DECIMAL(15,8),
    close DECIMAL(15,8),
    indicators JSONB DEFAULT '{}'::jsonb,
    sentiment_score DECIMAL(5,4),
    confluence_magnitude DECIMAL(5,4),
    confluence_vector DECIMAL(5,4)[] CHECK (array_length(confluence_vector, 1) = 3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_market_data_asset_time ON market_data(asset_id, timestamp DESC);
CREATE INDEX idx_market_data_timestamp ON market_data(timestamp DESC);

-- User Portfolios
CREATE TABLE portfolios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_public BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Portfolio Holdings
CREATE TABLE portfolio_holdings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID REFERENCES portfolios(id) ON DELETE CASCADE,
    asset_id UUID REFERENCES market_assets(id),
    quantity DECIMAL(20,8) NOT NULL,
    average_price DECIMAL(15,8),
    current_price DECIMAL(15,8),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Watchlists
CREATE TABLE watchlists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    asset_id UUID REFERENCES market_assets(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    alerts_enabled BOOLEAN DEFAULT true,
    alert_conditions JSONB DEFAULT '{}'::jsonb
);

-- Subscription Management
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    stripe_subscription_id VARCHAR(255),
    stripe_customer_id VARCHAR(255),
    plan_name VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL, -- active, canceled, past_due, etc.
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    cancel_at_period_end BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payment History
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subscription_id UUID REFERENCES subscriptions(id),
    stripe_payment_intent_id VARCHAR(255),
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    status VARCHAR(50) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- User Activity Tracking
CREATE TABLE user_activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    activity_type VARCHAR(100) NOT NULL,
    activity_data JSONB DEFAULT '{}'::jsonb,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_activities_user_time ON user_activities(user_id, created_at DESC);

-- AI Model Predictions
CREATE TABLE predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID REFERENCES market_assets(id),
    model_name VARCHAR(100) NOT NULL,
    prediction_type VARCHAR(50) NOT NULL, -- price, direction, volatility
    predicted_value DECIMAL(15,8),
    confidence_score DECIMAL(5,4),
    timeframe VARCHAR(20), -- 1h, 1d, 1w, etc.
    prediction_data JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    target_date TIMESTAMP NOT NULL
);

-- Correlation Analysis
CREATE TABLE asset_correlations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_a_id UUID REFERENCES market_assets(id),
    asset_b_id UUID REFERENCES market_assets(id),
    correlation_coefficient DECIMAL(5,4) NOT NULL,
    timeframe VARCHAR(20) NOT NULL,
    calculation_date DATE DEFAULT CURRENT_DATE,
    data_points INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_correlation UNIQUE (asset_a_id, asset_b_id, timeframe, calculation_date)
);

-- Functions and Triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_portfolios_updated_at BEFORE UPDATE ON portfolios 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscriptions_updated_at BEFORE UPDATE ON subscriptions 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Data retention policies (optional)
CREATE OR REPLACE FUNCTION cleanup_old_market_data()
RETURNS void AS $$
BEGIN
    -- Keep only 2 years of minute-level data
    DELETE FROM market_data 
    WHERE created_at < CURRENT_DATE - INTERVAL '2 years';
    
    -- Keep only 6 months of user activities
    DELETE FROM user_activities 
    WHERE created_at < CURRENT_DATE - INTERVAL '6 months';
END;
$$ LANGUAGE plpgsql;

-- Schedule cleanup (requires pg_cron extension)
-- SELECT cron.schedule('cleanup-old-data', '0 2 * * 0', 'SELECT cleanup_old_market_data();');`,

    'api-gateway': `// API Gateway with Authentication and Rate Limiting
// Node.js + Express + JWT Implementation

const express = require('express');
const jwt = require('jsonwebtoken');
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const { Pool } = require('pg');
const Redis = require('redis');
const winston = require('winston');

class APIGateway {
    constructor() {
        this.app = express();
        this.db = new Pool({
            connectionString: process.env.DATABASE_URL,
            ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
        });
        this.redis = Redis.createClient({ url: process.env.REDIS_URL });
        this.logger = winston.createLogger({
            level: 'info',
            format: winston.format.json(),
            transports: [
                new winston.transports.File({ filename: 'error.log', level: 'error' }),
                new winston.transports.File({ filename: 'combined.log' })
            ]
        });
        
        this.setupMiddleware();
        this.setupRoutes();
    }
    
    setupMiddleware() {
        // Security headers
        this.app.use(helmet({
            contentSecurityPolicy: {
                directives: {
                    defaultSrc: ["'self'"],
                    scriptSrc: ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com"],
                    styleSrc: ["'self'", "'unsafe-inline'"],
                    imgSrc: ["'self'", "data:", "https:"],
                    connectSrc: ["'self'", "wss:", "https:"]
                }
            }
        }));
        
        // CORS configuration
        this.app.use(cors({
            origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
            credentials: true,
            methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
            allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With']
        }));
        
        // Rate limiting
        const createRateLimit = (windowMs, max, message) => rateLimit({
            windowMs,
            max,
            message: { error: message },
            standardHeaders: true,
            legacyHeaders: false,
            keyGenerator: (req) => {
                return req.ip + ':' + (req.user?.id || 'anonymous');
            }
        });
        
        // Different limits for different endpoints
        this.app.use('/api/auth', createRateLimit(15 * 60 * 1000, 5, 'Too many auth attempts'));
        this.app.use('/api/market-data', createRateLimit(60 * 1000, 100, 'Market data rate limit exceeded'));
        this.app.use('/api', createRateLimit(15 * 60 * 1000, 1000, 'API rate limit exceeded'));
        
        // Body parsing
        this.app.use(express.json({ limit: '10mb' }));
        this.app.use(express.urlencoded({ extended: true, limit: '10mb' }));
        
        // Request logging
        this.app.use((req, res, next) => {
            this.logger.info({
                method: req.method,
                url: req.url,
                ip: req.ip,
                userAgent: req.get('User-Agent'),
                timestamp: new Date().toISOString()
            });
            next();
        });
    }
    
    setupRoutes() {
        // Health check
        this.app.get('/health', (req, res) => {
            res.json({ 
                status: 'healthy', 
                timestamp: new Date().toISOString(),
                version: process.env.APP_VERSION || '1.0.0'
            });
        });
        
        // Authentication routes
        this.app.post('/api/auth/register', this.register.bind(this));
        this.app.post('/api/auth/login', this.login.bind(this));
        this.app.post('/api/auth/refresh', this.refreshToken.bind(this));
        this.app.post('/api/auth/logout', this.authenticateToken.bind(this), this.logout.bind(this));
        
        // Protected routes
        this.app.use('/api/user', this.authenticateToken.bind(this));
        this.app.use('/api/portfolio', this.authenticateToken.bind(this));
        this.app.use('/api/predictions', this.authenticateToken.bind(this), this.requireSubscription.bind(this));
        
        // Market data routes (some public, some protected)
        this.app.get('/api/market-data/assets', this.getAssets.bind(this));
        this.app.get('/api/market-data/current/:symbol', this.getCurrentData.bind(this));
        this.app.get('/api/market-data/historical/:symbol', 
                    this.authenticateToken.bind(this), this.getHistoricalData.bind(this));
        
        // User management
        this.app.get('/api/user/profile', this.getProfile.bind(this));
        this.app.put('/api/user/profile', this.updateProfile.bind(this));
        this.app.get('/api/user/subscription', this.getSubscription.bind(this));
        
        // Error handling
        this.app.use(this.errorHandler.bind(this));
    }
    
    async register(req, res) {
        try {
            const { email, password, firstName, lastName } = req.body;
            
            // Validation
            if (!email || !password) {
                return res.status(400).json({ error: 'Email and password required' });
            }
            
            if (password.length < 8) {
                return res.status(400).json({ error: 'Password must be at least 8 characters' });
            }
            
            // Check if user exists
            const existingUser = await this.db.query(
                'SELECT id FROM users WHERE email = $1',
                [email.toLowerCase()]
            );
            
            if (existingUser.rows.length > 0) {
                return res.status(409).json({ error: 'User already exists' });
            }
            
            // Hash password
            const passwordHash = await bcrypt.hash(password, 12);
            
            // Create user
            const result = await this.db.query(
                \`INSERT INTO users (email, password_hash, first_name, last_name) 
                 VALUES ($1, $2, $3, $4) RETURNING id, email, first_name, last_name\`,
                [email.toLowerCase(), passwordHash, firstName, lastName]
            );
            
            const user = result.rows[0];
            
            // Generate tokens
            const accessToken = this.generateAccessToken(user);
            const refreshToken = this.generateRefreshToken(user);
            
            // Store refresh token
            await this.storeRefreshToken(user.id, refreshToken, req);
            
            res.json({
                message: 'Login successful',
                user: {
                    id: user.id,
                    email: user.email,
                    firstName: user.first_name,
                    lastName: user.last_name,
                    subscriptionTier: user.subscription_tier
                },
                accessToken,
                refreshToken
            });
            
        } catch (error) {
            this.logger.error('Login error:', error);
            res.status(500).json({ error: 'Internal server error' });
        }
    }
    
    generateAccessToken(user) {
        return jwt.sign(
            { 
                userId: user.id, 
                email: user.email,
                subscriptionTier: user.subscription_tier || 'basic'
            },
            process.env.JWT_SECRET,
            { expiresIn: '15m' }
        );
    }
    
    generateRefreshToken(user) {
        return jwt.sign(
            { userId: user.id, tokenType: 'refresh' },
            process.env.JWT_REFRESH_SECRET,
            { expiresIn: '7d' }
        );
    }
    
    async authenticateToken(req, res, next) {
        const authHeader = req.headers['authorization'];
        const token = authHeader && authHeader.split(' ')[1];
        
        if (!token) {
            return res.status(401).json({ error: 'Access token required' });
        }
        
        try {
            const decoded = jwt.verify(token, process.env.JWT_SECRET);
            
            // Get fresh user data
            const result = await this.db.query(
                'SELECT id, email, subscription_tier, is_active FROM users WHERE id = $1',
                [decoded.userId]
            );
            
            if (result.rows.length === 0 || !result.rows[0].is_active) {
                return res.status(401).json({ error: 'Invalid token' });
            }
            
            req.user = result.rows[0];
            next();
            
        } catch (error) {
            if (error.name === 'TokenExpiredError') {
                return res.status(401).json({ error: 'Token expired' });
            }
            return res.status(403).json({ error: 'Invalid token' });
        }
    }
    
    requireSubscription(req, res, next) {
        const tier = req.user.subscription_tier;
        if (tier === 'basic' || !tier) {
            return res.status(403).json({ 
                error: 'Premium subscription required',
                upgradeUrl: '/subscription/upgrade'
            });
        }
        next();
    }
    
    errorHandler(error, req, res, next) {
        this.logger.error('API Error:', {
            error: error.message,
            stack: error.stack,
            url: req.url,
            method: req.method,
            user: req.user?.id
        });
        
        res.status(500).json({ 
            error: 'Internal server error',
            requestId: req.id || 'unknown'
        });
    }
}

module.exports = APIGateway;`,

    'data-pipeline': `// Enhanced Real-time Data Pipeline
// Node.js with WebSocket support and data validation

const WebSocket = require('ws');
const EventEmitter = require('events');
const Redis = require('redis');
const { Pool } = require('pg');
const axios = require('axios');
const winston = require('winston');

class MarketDataPipeline extends EventEmitter {
    constructor() {
        super();
        this.db = new Pool({ connectionString: process.env.DATABASE_URL });
        this.redis = Redis.createClient({ url: process.env.REDIS_URL });
        this.wss = new WebSocket.Server({ port: process.env.WS_PORT || 8080 });
        
        this.dataSources = {
            yfinance: new YahooFinanceSource(),
            coingecko: new CoinGeckoSource(),
            alphavantage: new AlphaVantageSource(),
            newsapi: new NewsAPISource()
        };
        
        this.subscriptions = new Map(); // symbol -> Set of websocket connections
        this.dataCache = new Map();
        this.failoverState = new Map(); // Track failed sources
        
        this.logger = winston.createLogger({
            level: 'info',
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.json()
            ),
            transports: [
                new winston.transports.Console(),
                new winston.transports.File({ filename: 'data-pipeline.log' })
            ]
        });
        
        this.setupWebSocketServer();
        this.startDataCollection();
        this.setupHealthMonitoring();
    }
    
    setupWebSocketServer() {
        this.wss.on('connection', (ws, req) => {
            this.logger.info('New WebSocket connection', { ip: req.socket.remoteAddress });
            
            ws.on('message', (message) => {
                try {
                    const data = JSON.parse(message);
                    this.handleWebSocketMessage(ws, data);
                } catch (error) {
                    ws.send(JSON.stringify({ error: 'Invalid JSON' }));
                }
            });
            
            ws.on('close', () => {
                this.removeSubscriptions(ws);
            });
            
            ws.on('error', (error) => {
                this.logger.error('WebSocket error:', error);
            });
            
            // Send initial connection success
            ws.send(JSON.stringify({ 
                type: 'connection', 
                status: 'connected',
                timestamp: new Date().toISOString()
            }));
        });
    }
    
    handleWebSocketMessage(ws, data) {
        switch (data.type) {
            case 'subscribe':
                this.addSubscription(ws, data.symbols);
                break;
                
            case 'unsubscribe':
                this.removeSubscription(ws, data.symbols);
                break;
                
            case 'get_historical':
                this.sendHistoricalData(ws, data.symbol, data.timeframe);
                break;
                
            default:
                ws.send(JSON.stringify({ error: 'Unknown message type' }));
        }
    }
    
    addSubscription(ws, symbols) {
        if (!Array.isArray(symbols)) symbols = [symbols];
        
        symbols.forEach(symbol => {
            if (!this.subscriptions.has(symbol)) {
                this.subscriptions.set(symbol, new Set());
            }
            this.subscriptions.get(symbol).add(ws);
        });
        
        ws.send(JSON.stringify({ 
            type: 'subscribed', 
            symbols,
            timestamp: new Date().toISOString()
        }));
        
        // Send current data immediately
        symbols.forEach(symbol => {
            const cachedData = this.dataCache.get(symbol);
            if (cachedData) {
                ws.send(JSON.stringify({
                    type: 'market_data',
                    symbol,
                    data: cachedData,
                    timestamp: new Date().toISOString()
                }));
            }
        });
    }
    
    async startDataCollection() {
        // Get list of active assets from database
        const assetsResult = await this.db.query(
            'SELECT symbol, asset_type FROM market_assets WHERE is_active = true'
        );
        
        const assets = assetsResult.rows;
        this.logger.info(\`Starting data collection for \${assets.length} assets\`);
        
        // Start collection intervals
        setInterval(() => this.collectMarketData(assets), 30000); // Every 30 seconds
        setInterval(() => this.collectNewsData(assets), 300000); // Every 5 minutes
        setInterval(() => this.calculateIndicators(), 60000); // Every minute
        
        // Initial data collection
        await this.collectMarketData(assets);
    }
    
    async collectMarketData(assets) {
        const promises = assets.map(asset => this.fetchAssetData(asset));
        const results = await Promise.allSettled(promises);
        
        let successCount = 0;
        let failureCount = 0;
        
        results.forEach((result, index) => {
            if (result.status === 'fulfilled' && result.value) {
                successCount++;
                this.processMarketData(assets[index], result.value);
            } else {
                failureCount++;
                this.logger.error(\`Failed to fetch data for \${assets[index].symbol}\`, result.reason);
            }
        });
        
        this.logger.info(\`Data collection complete: \${successCount} success, \${failureCount} failures\`);
    }
    
    async fetchAssetData(asset) {
        const sources = this.getSourcesForAsset(asset);
        
        for (const sourceName of sources) {
            const source = this.dataSources[sourceName];
            if (!source || this.failoverState.get(sourceName)) {
                continue; // Skip failed sources
            }
            
            try {
                const data = await source.fetchData(asset.symbol, asset.asset_type);
                if (data && this.validateMarketData(data)) {
                    // Mark source as healthy
                    this.failoverState.delete(sourceName);
                    return { source: sourceName, data };
                }
            } catch (error) {
                this.logger.warn(\`Source \${sourceName} failed for \${asset.symbol}\`, error.message);
                this.markSourceFailed(sourceName);
            }
        }
        
        throw new Error(\`All sources failed for \${asset.symbol}\`);
    }
    
    validateMarketData(data) {
        // Comprehensive data validation
        const required = ['price', 'volume', 'timestamp'];
        for (const field of required) {
            if (data[field] === undefined || data[field] === null) {
                return false;
            }
        }
        
        // Validate price is reasonable (not zero, not negative, not extremely large)
        if (data.price <= 0 || data.price > 1000000) {
            return false;
        }
        
        // Validate volume is non-negative
        if (data.volume < 0) {
            return false;
        }
        
        // Validate timestamp is recent (within last hour)
        const hourAgo = Date.now() - (60 * 60 * 1000);
        if (new Date(data.timestamp).getTime() < hourAgo) {
            return false;
        }
        
        return true;
    }
    
    async processMarketData(asset, { source, data }) {
        try {
            // Calculate technical indicators
            const indicators = await this.calculateTechnicalIndicators(asset.symbol, data);
            
            // Get sentiment score
            const sentiment = await this.getSentimentScore(asset.symbol);
            
            // Calculate confluence
            const confluence = this.calculateConfluence(indicators);
            
            const enrichedData = {
                ...data,
                indicators,
                sentiment,
                confluence_magnitude: confluence.magnitude,
                confluence_vector: confluence.vector,
                source,
                processed_at: new Date().toISOString()
            };
            
            // Store in database
            await this.storeMarketData(asset, enrichedData);
            
            // Cache for immediate access
            this.dataCache.set(asset.symbol, enrichedData);
            
            // Broadcast to WebSocket subscribers
            this.broadcastToSubscribers(asset.symbol, enrichedData);
            
            // Cache in Redis for other services
            await this.redis.setex(
                \`market_data:\${asset.symbol}\`,
                300, // 5 minutes
                JSON.stringify(enrichedData)
            );
            
        } catch (error) {
            this.logger.error(\`Error processing data for \${asset.symbol}\`, error);
        }
    }
    
    async calculateTechnicalIndicators(symbol, currentData) {
        // Get historical data for calculations
        const historicalResult = await this.db.query(
            \`SELECT price, volume, timestamp, high, low, open, close 
             FROM market_data 
             WHERE asset_id = (SELECT id FROM market_assets WHERE symbol = $1)
             ORDER BY timestamp DESC 
             LIMIT 50\`,
            [symbol]
        );
        
        const historical = historicalResult.rows;
        if (historical.length < 14) {
            return {}; // Not enough data for indicators
        }
        
        const prices = historical.map(h => h.close || h.price).reverse();
        const volumes = historical.map(h => h.volume).reverse();
        const highs = historical.map(h => h.high || h.price).reverse();
        const lows = historical.map(h => h.low || h.price).reverse();
        
        return {
            rsi: this.calculateRSI(prices),
            macd: this.calculateMACD(prices),
            bb_squeeze: this.calculateBollingerBands(prices),
            stochastic: this.calculateStochastic(highs, lows, prices),
            ema_cross: this.calculateEMACross(prices),
            volume_profile: this.calculateVolumeProfile(volumes),
            momentum: this.calculateMomentum(prices),
            volatility: this.calculateVolatility(prices)
        };
    }
    
    calculateRSI(prices, period = 14) {
        if (prices.length < period + 1) return null;
        
        const deltas = [];
        for (let i = 1; i < prices.length; i++) {
            deltas.push(prices[i] - prices[i - 1]);
        }
        
        const gains = deltas.map(d => d > 0 ? d : 0);
        const losses = deltas.map(d => d < 0 ? -d : 0);
        
        const avgGain = gains.slice(-period).reduce((a, b) => a + b) / period;
        const avgLoss = losses.slice(-period).reduce((a, b) => a + b) / period;
        
        if (avgLoss === 0) return 100;
        const rs = avgGain / avgLoss;
        return 100 - (100 / (1 + rs));
    }
    
    calculateMACD(prices) {
        if (prices.length < 26) return null;
        
        const ema12 = this.calculateEMA(prices, 12);
        const ema26 = this.calculateEMA(prices, 26);
        
        if (!ema12 || !ema26) return null;
        
        const macdLine = ema12 - ema26;
        return macdLine;
    }
    
    calculateEMA(prices, period) {
        if (prices.length < period) return null;
        
        const multiplier = 2 / (period + 1);
        let ema = prices.slice(0, period).reduce((a, b) => a + b) / period;
        
        for (let i = period; i < prices.length; i++) {
            ema = (prices[i] * multiplier) + (ema * (1 - multiplier));
        }
        
        return ema;
    }
    
    broadcastToSubscribers(symbol, data) {
        const subscribers = this.subscriptions.get(symbol);
        if (!subscribers || subscribers.size === 0) return;
        
        const message = JSON.stringify({
            type: 'market_data',
            symbol,
            data,
            timestamp: new Date().toISOString()
        });
        
        subscribers.forEach(ws => {
            if (ws.readyState === WebSocket.OPEN) {
                ws.send(message);
            } else {
                subscribers.delete(ws);
            }
        });
    }
    
    setupHealthMonitoring() {
        // Check source health every 5 minutes
        setInterval(() => {
            this.checkSourceHealth();
        }, 300000);
        
        // Clean failed source states every hour
        setInterval(() => {
            this.cleanFailoverState();
        }, 3600000);
    }
    
    async checkSourceHealth() {
        for (const [sourceName, source] of Object.entries(this.dataSources)) {
            try {
                const healthCheck = await source.healthCheck();
                if (healthCheck) {
                    this.failoverState.delete(sourceName);
                    this.logger.info(\`Source \${sourceName} is healthy\`);
                } else {
                    this.markSourceFailed(sourceName);
                }
            } catch (error) {
                this.markSourceFailed(sourceName);
                this.logger.error(\`Source \${sourceName} health check failed\`, error);
            }
        }
    }
    
    markSourceFailed(sourceName) {
        this.failoverState.set(sourceName, {
            failedAt: new Date(),
            retryAfter: new Date(Date.now() + 300000) // Retry after 5 minutes
        });
    }
    
    getSourcesForAsset(asset) {
        // Define source priority by asset type
        const sourceMapping = {
            stocks: ['yfinance', 'alphavantage'],
            crypto_coins: ['coingecko', 'yfinance'],
            fx_pairs: ['yfinance', 'alphavantage'],
            precious_metals: ['yfinance', 'alphavantage'],
            futures: ['yfinance']
        };
        
        return sourceMapping[asset.asset_type] || ['yfinance'];
    }
}

// Data source implementations
class YahooFinanceSource {
    async fetchData(symbol, assetType) {
        const url = \`https://query1.finance.yahoo.com/v8/finance/chart/\${symbol}\`;
        const response = await axios.get(url, { timeout: 10000 });
        
        const chart = response.data.chart.result[0];
        const quote = chart.indicators.quote[0];
        const timestamp = chart.timestamp[chart.timestamp.length - 1] * 1000;
        
        return {
            price: quote.close[quote.close.length - 1],
            open: quote.open[quote.open.length - 1],
            high: quote.high[quote.high.length - 1],
            low: quote.low[quote.low.length - 1],
            volume: quote.volume[quote.volume.length - 1],
            timestamp: new Date(timestamp).toISOString()
        };
    }
    
    async healthCheck() {
        try {
            await axios.get('https://query1.finance.yahoo.com/v8/finance/chart/AAPL', { timeout: 5000 });
            return true;
        } catch {
            return false;
        }
    }
}

class CoinGeckoSource {
    async fetchData(symbol, assetType) {
        if (assetType !== 'crypto_coins') return null;
        
        const url = \`https://api.coingecko.com/api/v3/simple/price?ids=\${symbol}&vs_currencies=usd&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true\`;
        const response = await axios.get(url, { timeout: 10000 });
        
        const data = response.data[symbol];
        if (!data) return null;
        
        return {
            price: data.usd,
            volume: data.usd_24h_vol,
            change_24h: data.usd_24h_change,
            timestamp: new Date(data.last_updated_at * 1000).toISOString()
        };
    }
    
    async healthCheck() {
        try {
            await axios.get('https://api.coingecko.com/api/v3/ping', { timeout: 5000 });
            return true;
        } catch {
            return false;
        }
    }
}

module.exports = MarketDataPipeline;`
          }
        ]
    }
  ];

  const getTaskProgress = (taskId) => {
    return taskProgress[taskId] || 0;
  };

  const isTaskCompleted = (taskId) => {
    return completedTasks.has(taskId);
  };

  const isTaskActive = (taskId) => {
    return activeTasks.has(taskId);
  };

  const canStartTask = (task) => {
    return task.dependencies.every(dep => isTaskCompleted(dep));
  };

  const executeTask = async (taskId) => {
    if (!canStartTask(projectPhases.flatMap(p => p.tasks).find(t => t.id === taskId))) {
      return;
    }

    setActiveTasks(prev => new Set([...prev, taskId]));
    
    // Simulate task execution with progress updates
    for (let progress = 0; progress <= 100; progress += 10) {
      setTaskProgress(prev => ({ ...prev, [taskId]: progress }));
      await new Promise(resolve => setTimeout(resolve, 200));
    }

    setActiveTasks(prev => {
      const newSet = new Set(prev);
      newSet.delete(taskId);
      return newSet;
    });
    
    setCompletedTasks(prev => new Set([...prev, taskId]));
  };

  const generateCode = (template) => {
    const code = codeTemplates[template] || '// Code template not found';
    setGeneratedCode(code);
  };

  const executePhase = async (phaseId) => {
    setIsExecuting(true);
    const phase = projectPhases.find(p => p.id === phaseId);
    
    for (const task of phase.tasks) {
      if (canStartTask(task)) {
        await executeTask(task.id);
      }
    }
    
    setIsExecuting(false);
  };

  const TaskCard = ({ task, phaseId }) => {
    const progress = getTaskProgress(task.id);
    const completed = isTaskCompleted(task.id);
    const active = isTaskActive(task.id);
    const canStart = canStartTask(task);

    return (
      <div className={`p-4 border rounded-lg transition-all ${
        completed ? 'bg-green-50 border-green-200' : 
        active ? 'bg-blue-50 border-blue-200 shadow-md' :
        canStart ? 'bg-white border-gray-200 hover:border-blue-300' :
        'bg-gray-50 border-gray-200 opacity-60'
      }`}>
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-2">
            {completed ? (
              <CheckCircle className="w-5 h-5 text-green-500" />
            ) : active ? (
              <Clock className="w-5 h-5 text-blue-500 animate-pulse" />
            ) : canStart ? (
              <Circle className="w-5 h-5 text-gray-400" />
            ) : (
              <AlertCircle className="w-5 h-5 text-gray-300" />
            )}
            <h4 className="font-medium text-sm">{task.name}</h4>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-xs text-gray-500">{task.duration}</span>
            {canStart && !completed && !active && (
              <button
                onClick={() => executeTask(task.id)}
                className="p-1 text-blue-500 hover:text-blue-700"
                title="Start Task"
              >
                <Play className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
        
        <p className="text-xs text-gray-600 mb-2">{task.description}</p>
        
        {active && (
          <div className="mb-2">
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <p className="text-xs text-gray-500 mt-1">{progress}% complete</p>
          </div>
        )}
        
        <div className="flex flex-wrap gap-1 mb-2">
          {task.deliverables.map((deliverable, idx) => (
            <span key={idx} className="px-2 py-1 bg-gray-100 text-xs rounded">
              {deliverable}
            </span>
          ))}
        </div>
        
        {task.codeTemplate && (
          <button
            onClick={() => {
              setSelectedTask(task);
              generateCode(task.codeTemplate);
            }}
            className="flex items-center space-x-1 text-xs text-purple-600 hover:text-purple-800"
          >
            <Code className="w-3 h-3" />
            <span>Generate Code</span>
          </button>
        )}
        
        {task.dependencies.length > 0 && (
          <div className="mt-2 pt-2 border-t border-gray-100">
            <p className="text-xs text-gray-500">
              Depends on: {task.dependencies.join(', ')}
            </p>
          </div>
        )}
      </div>
    );
  };

  const PhaseCard = ({ phase }) => {
    const phaseTasks = phase.tasks;
    const completedTasksCount = phaseTasks.filter(t => isTaskCompleted(t.id)).length;
    const totalTasks = phaseTasks.length;
    const phaseProgress = (completedTasksCount / totalTasks) * 100;

    return (
      <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              {phase.icon}
            </div>
            <div>
              <h3 className="font-semibold text-lg">{phase.name}</h3>
              <div className="flex items-center space-x-4 text-sm text-gray-600">
                <span>{phase.duration}</span>
                <span>{phase.cost}</span>
                <span className={`px-2 py-1 rounded text-xs ${
                  phase.priority === 'Critical' ? 'bg-red-100 text-red-700' :
                  phase.priority === 'High' ? 'bg-orange-100 text-orange-700' :
                  'bg-green-100 text-green-700'
                }`}>
                  {phase.priority}
                </span>
              </div>
            </div>
          </div>
          
          <div className="text-right">
            <div className="text-2xl font-bold text-gray-800">
              {completedTasksCount}/{totalTasks}
            </div>
            <div className="text-xs text-gray-500">Tasks Complete</div>
            <button
              onClick={() => executePhase(phase.id)}
              disabled={isExecuting || phaseProgress === 100}
              className={`mt-2 px-4 py-2 rounded-lg text-sm font-medium ${
                phaseProgress === 100 
                  ? 'bg-green-100 text-green-700 cursor-default'
                  : 'bg-blue-500 text-white hover:bg-blue-600 disabled:opacity-50'
              }`}
            >
              {phaseProgress === 100 ? 'Complete' : 'Execute Phase'}
            </button>
          </div>
        </div>

        <p className="text-gray-600 text-sm mb-4">{phase.description}</p>

        <div className="mb-4">
          <div className="flex items-center justify-between text-sm mb-1">
            <span>Phase Progress</span>
            <span>{Math.round(phaseProgress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-500 h-2 rounded-full transition-all duration-500"
              style={{ width: `${phaseProgress}%` }}
            ></div>
          </div>
        </div>

        <div className="grid gap-3">
          {phaseTasks.map(task => (
            <TaskCard key={task.id} task={task} phaseId={phase.id} />
          ))}
        </div>
      </div>
    );
  };

  const overallProgress = () => {
    const totalTasks = projectPhases.reduce((sum, phase) => sum + phase.tasks.length, 0);
    const completedCount = completedTasks.size;
    return (completedCount / totalTasks) * 100;
  };

  const totalCost = projectPhases.reduce((sum, phase) => {
    return sum + parseInt(phase.cost.replace(/[$,]/g, ''));
  }, 0);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Financial Market 2.0 - Project Execution Center
          </h1>
          <p className="text-gray-600">
            Complete development pipeline from concept to production deployment
          </p>
        </div>

        {/* Overall Progress */}
        <div className="bg-white rounded-xl p-6 mb-8 shadow-sm border border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Overall Progress</h3>
              <div className="text-2xl font-bold text-blue-600">
                {Math.round(overallProgress())}%
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${overallProgress()}%` }}
                ></div>
              </div>
            </div>
            
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Total Investment</h3>
              <div className="text-2xl font-bold text-green-600">
                ${totalCost.toLocaleString()}
              </div>
              <div className="text-sm text-gray-500 mt-2">Production Ready</div>
            </div>
            
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Token = this.generateRefreshToken(user);
            
            // Store refresh token
            await this.storeRefreshToken(user.id, refreshToken, req);
            
            res.status(201).json({
                message: 'User created successfully',
                user: {
                    id: user.id,
                    email: user.email,
                    firstName: user.first_name,
                    lastName: user.last_name
                },
                accessToken,
                refreshToken
            });
            
        } catch (error) {
            this.logger.error('Registration error:', error);
            res.status(500).json({ error: 'Internal server error' });
        }
    }
    
    async login(req, res) {
        try {
            const { email, password } = req.body;
            
            // Get user
            const result = await this.db.query(
                \`SELECT id, email, password_hash, first_name, last_name, 
                        subscription_tier, is_active 
                 FROM users WHERE email = $1\`,
                [email.toLowerCase()]
            );
            
            if (result.rows.length === 0) {
                return res.status(401).json({ error: 'Invalid credentials' });
            }
            
            const user = result.rows[0];
            
            if (!user.is_active) {
                return res.status(401).json({ error: 'Account disabled' });
            }
            
            // Verify password
            const passwordValid = await bcrypt.compare(password, user.password_hash);
            if (!passwordValid) {
                return res.status(401).json({ error: 'Invalid credentials' });
            }
            
            // Update last login
            await this.db.query(
                'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = $1',
                [user.id]
            );
            
            // Generate tokens
            const accessToken = this.generateAccessToken(user);
            const refresh
