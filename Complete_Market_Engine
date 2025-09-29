import os
import pandas as pd
import yfinance as yf
import requests
import numpy as np
from functools import reduce
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Advanced analysis imports
from scipy.fft import fft
from scipy.stats import pearsonr
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time

class FinancialMarketEngine:
    def __init__(self, data_dir="data", news_api_key=None):
        self.data_dir = data_dir
        self.news_api_key = news_api_key
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize sentiment analyzer
        self.analyzer = SentimentIntensityAnalyzer()
        
        # Asset configurations
        self.asset_config = {
            'stocks': ["^GSPC", "^DJI", "^IXIC", "AAPL", "MSFT", "GOOGL", "TSLA"],
            'fx_pairs': ["DX-Y.NYB", "EURUSD=X", "GBPUSD=X", "USDJPY=X"],
            'crypto_coins': ["bitcoin", "ethereum", "cardano", "solana"],
            'precious_metals': ["GC=F", "SI=F", "PL=F"],  # Gold, Silver, Platinum futures
            'futures': ["CL=F", "NG=F", "ZC=F"]  # Oil, Natural Gas, Corn
        }
        
        # Adaptive weights system
        self.adaptive_weights = {}
        self.initialize_weights()
        
        # Market data storage
        self.market_data = {}
        self.indicators = {}
        self.sentiment_scores = {}
        self.correlations = {}
        
    def initialize_weights(self):
        """Initialize adaptive weights for all indicators"""
        indicators = ['rsi', 'macd', 'bb_squeeze', 'stochastic', 'ema_cross', 
                     'volume_profile', 'momentum', 'volatility']
        
        for asset_type in self.asset_config.keys():
            self.adaptive_weights[asset_type] = {
                indicator: 1.0 / len(indicators) for indicator in indicators
            }

    def fetch_yfinance_data(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        """Enhanced Yahoo Finance data fetching with error handling"""
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, auto_adjust=True)
            
            if df.empty:
                print(f"Warning: No data retrieved for {ticker}")
                return pd.DataFrame()
                
            df = df.reset_index()
            df['Symbol'] = ticker
            return df
            
        except Exception as e:
            print(f"Error fetching {ticker}: {str(e)}")
            return pd.DataFrame()

    def fetch_crypto_data(self, coin_id: str, days: int = 365) -> pd.DataFrame:
        """Fetch cryptocurrency data from CoinGecko with enhanced metrics"""
        try:
            # Historical prices
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'daily'
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'prices' not in data:
                print(f"Warning: No price data for {coin_id}")
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(data['prices'], columns=['timestamp', 'Close'])
            df['Date'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['Symbol'] = coin_id
            
            # Add volume if available
            if 'total_volumes' in data:
                volumes = pd.DataFrame(data['total_volumes'], columns=['timestamp', 'Volume'])
                df = df.merge(volumes, on='timestamp', how='left')
            
            df = df.drop('timestamp', axis=1)
            return df
            
        except Exception as e:
            print(f"Error fetching crypto data for {coin_id}: {str(e)}")
            return pd.DataFrame()

    def fetch_news_sentiment(self, asset: str, max_articles: int = 50) -> float:
        """Fetch and analyze news sentiment for an asset"""
        if not self.news_api_key:
            return 0.0
            
        try:
            # Clean asset name for search
            search_term = asset.replace('^', '').replace('=X', '').replace('=F', '')
            
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': search_term,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': max_articles,
                'apiKey': self.news_api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'articles' not in data:
                return 0.0
            
            sentiments = []
            for article in data['articles']:
                title = article.get('title', '')
                description = article.get('description', '')
                text = f"{title} {description}"
                
                if text.strip():
                    sentiment = self.analyzer.polarity_scores(text)
                    sentiments.append(sentiment['compound'])
            
            return np.mean(sentiments) if sentiments else 0.0
            
        except Exception as e:
            print(f"Error fetching sentiment for {asset}: {str(e)}")
            return 0.0

    def calculate_technical_indicators(self, df: pd.DataFrame) -> Dict:
        """Calculate comprehensive technical indicators"""
        if df.empty or 'Close' not in df.columns:
            return {}
            
        close = df['Close']
        high = df.get('High', close)
        low = df.get('Low', close)
        volume = df.get('Volume', pd.Series([1] * len(close)))
        
        indicators = {}
        
        # RSI
        def calculate_rsi(prices, period=14):
            delta = prices.diff()
            gain = delta.clip(lower=0)
            loss = -1 * delta.clip(upper=0)
            avg_gain = gain.rolling(period).mean()
            avg_loss = loss.rolling(period).mean()
            rs = avg_gain / avg_loss
            return 100 - (100 / (1 + rs))
        
        indicators['rsi'] = calculate_rsi(close).iloc[-1] if len(close) > 14 else 50
        
        # MACD
        ema12 = close.ewm(span=12).mean()
        ema26 = close.ewm(span=26).mean()
        macd_line = ema12 - ema26
        signal_line = macd_line.ewm(span=9).mean()
        indicators['macd'] = (macd_line.iloc[-1] - signal_line.iloc[-1]) if len(close) > 26 else 0
        
        # Bollinger Bands Squeeze
        sma20 = close.rolling(20).mean()
        bb_upper = sma20 + (close.rolling(20).std() * 2)
        bb_lower = sma20 - (close.rolling(20).std() * 2)
        bb_squeeze = (bb_upper.iloc[-1] - bb_lower.iloc[-1]) / sma20.iloc[-1] if len(close) > 20 else 0.1
        indicators['bb_squeeze'] = bb_squeeze
        
        # Stochastic
        lowest_low = low.rolling(14).min()
        highest_high = high.rolling(14).max()
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        indicators['stochastic'] = k_percent.iloc[-1] if len(close) > 14 else 50
        
        # EMA Crossover
        ema_fast = close.ewm(span=12).mean()
        ema_slow = close.ewm(span=26).mean()
        indicators['ema_cross'] = (ema_fast.iloc[-1] - ema_slow.iloc[-1]) / close.iloc[-1] if len(close) > 26 else 0
        
        # Volume Profile (simplified)
        avg_volume = volume.rolling(20).mean()
        indicators['volume_profile'] = (volume.iloc[-1] - avg_volume.iloc[-1]) / avg_volume.iloc[-1] if len(volume) > 20 else 0
        
        # Momentum
        indicators['momentum'] = (close.iloc[-1] - close.iloc[-10]) / close.iloc[-10] if len(close) > 10 else 0
        
        # Volatility (ATR-based)
        tr1 = high - low
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))
        true_range = pd.DataFrame([tr1, tr2, tr3]).max()
        indicators['volatility'] = true_range.rolling(14).mean().iloc[-1] / close.iloc[-1] if len(close) > 14 else 0.02
        
        return indicators

    def calculate_geometric_entropy(self, price_series: pd.Series) -> float:
        """Calculate geometric entropy for chaos measurement"""
        if len(price_series) < 10:
            return 0.5
            
        returns = price_series.pct_change().dropna()
        if len(returns) == 0:
            return 0.5
            
        # Create histogram of returns
        hist, _ = np.histogram(returns, bins=10, density=True)
        hist = hist[hist > 0]  # Remove zero bins
        
        if len(hist) == 0:
            return 0.5
            
        # Calculate entropy
        entropy = -np.sum(hist * np.log(hist))
        return min(entropy / np.log(len(hist)), 1.0)  # Normalize

    def calculate_confluence_score(self, indicators: Dict, weights: Dict) -> Tuple[float, np.ndarray]:
        """Calculate confluence vector magnitude and direction"""
        if not indicators or not weights:
            return 0.0, np.array([0, 0, 0])
        
        # Normalize indicators to [-1, 1] range
        normalized = {}
        normalized['rsi'] = (indicators.get('rsi', 50) - 50) / 50
        normalized['macd'] = np.tanh(indicators.get('macd', 0) * 100)
        normalized['stochastic'] = (indicators.get('stochastic', 50) - 50) / 50
        normalized['ema_cross'] = np.tanh(indicators.get('ema_cross', 0) * 100)
        normalized['momentum'] = np.tanh(indicators.get('momentum', 0) * 10)
        
        # Create 3D vector
        vector = np.array([0.0, 0.0, 0.0])
        total_weight = 0
        
        for indicator, value in normalized.items():
            if indicator in weights:
                weight = weights[indicator]
                # Map to 3D space
                angle = hash(indicator) % 360 * np.pi / 180
                vector[0] += weight * value * np.cos(angle)
                vector[1] += weight * value * np.sin(angle)
                vector[2] += weight * value * np.cos(angle * 2)
                total_weight += weight
        
        if total_weight > 0:
            vector /= total_weight
        
        magnitude = np.linalg.norm(vector)
        return magnitude, vector

    def calculate_cross_asset_resonance(self, series_a: pd.Series, series_b: pd.Series) -> float:
        """Calculate cross-asset resonance using FFT"""
        if len(series_a) != len(series_b) or len(series_a) < 10:
            return 0.0
        
        try:
            # Normalize series
            a_norm = (series_a - series_a.mean()) / series_a.std()
            b_norm = (series_b - series_b.mean()) / series_b.std()
            
            # Calculate FFT
            fa = fft(a_norm.fillna(0))
            fb = fft(b_norm.fillna(0))
            
            # Calculate cross-power spectrum
            cross_power = fa * np.conj(fb)
            resonance = np.abs(cross_power).mean()
            
            return min(resonance, 1.0)  # Cap at 1.0
            
        except Exception as e:
            print(f"Error calculating resonance: {str(e)}")
            return 0.0

    def update_adaptive_weights(self, asset_type: str, indicators: Dict, performance_feedback: float = None):
        """Update adaptive weights based on indicator performance"""
        if asset_type not in self.adaptive_weights:
            return
        
        current_weights = self.adaptive_weights[asset_type]
        alpha = 0.1  # Learning rate
        
        # Calculate information gain for each indicator
        info_gains = {}
        for indicator, value in indicators.items():
            if indicator in current_weights:
                # Simple info gain based on deviation from neutral
                if indicator == 'rsi':
                    info_gains[indicator] = abs(value - 50) / 50
                elif indicator == 'stochastic':
                    info_gains[indicator] = abs(value - 50) / 50
                else:
                    info_gains[indicator] = min(abs(value) * 10, 1.0)
        
        # Normalize info gains
        total_gain = sum(info_gains.values()) or 1.0
        for indicator in info_gains:
            info_gains[indicator] /= total_gain
        
        # Update weights
        for indicator in current_weights:
            if indicator in info_gains:
                new_weight = alpha * info_gains[indicator] + (1 - alpha) * current_weights[indicator]
                current_weights[indicator] = new_weight
        
        # Renormalize weights
        total_weight = sum(current_weights.values()) or 1.0
        for indicator in current_weights:
            current_weights[indicator] /= total_weight

    def process_all_assets(self) -> Dict:
        """Process all configured assets and generate complete market data"""
        all_data = {}
        
        print("🔄 Processing market data...")
        
        for asset_type, assets in self.asset_config.items():
            print(f"Processing {asset_type}...")
            type_data = {}
            
            for asset in assets:
                try:
                    # Fetch data based on asset type
                    if asset_type == 'crypto_coins':
                        df = self.fetch_crypto_data(asset)
                    else:
                        df = self.fetch_yfinance_data(asset)
                    
                    if df.empty:
                        continue
                    
                    # Calculate indicators
                    indicators = self.calculate_technical_indicators(df)
                    
                    # Get sentiment
                    sentiment = self.fetch_news_sentiment(asset)
                    
                    # Calculate geometric entropy
                    entropy = self.calculate_geometric_entropy(df['Close']) if 'Close' in df.columns else 0.5
                    
                    # Update adaptive weights
                    self.update_adaptive_weights(asset_type, indicators)
                    
                    # Calculate confluence
                    weights = self.adaptive_weights[asset_type]
                    confluence_magnitude, confluence_vector = self.calculate_confluence_score(indicators, weights)
                    
                    # Store processed data
                    asset_data = {
                        'symbol': asset,
                        'current_price': df['Close'].iloc[-1] if 'Close' in df.columns else 0,
                        'price_change_24h': ((df['Close'].iloc[-1] / df['Close'].iloc[-2]) - 1) * 100 if len(df) > 1 and 'Close' in df.columns else 0,
                        'volume': df['Volume'].iloc[-1] if 'Volume' in df.columns else 0,
                        'indicators': indicators,
                        'sentiment': sentiment,
                        'entropy': entropy,
                        'confluence_magnitude': confluence_magnitude,
                        'confluence_vector': confluence_vector.tolist(),
                        'weights': weights.copy(),
                        'last_updated': datetime.now().isoformat()
                    }
                    
                    type_data[asset] = asset_data
                    
                except Exception as e:
                    print(f"Error processing {asset}: {str(e)}")
                    continue
            
            all_data[asset_type] = type_data
        
        # Calculate cross-asset correlations
        print("🔄 Calculating cross-asset correlations...")
        self.calculate_all_correlations(all_data)
        
        # Save processed data
        self.save_processed_data(all_data)
        
        print("✅ Market data processing complete!")
        return all_data

    def calculate_all_correlations(self, market_data: Dict):
        """Calculate correlations between all asset pairs"""
        self.correlations = {}
        
        # Flatten all assets for correlation calculation
        all_assets = {}
        for asset_type, assets in market_data.items():
            for symbol, data in assets.items():
                all_assets[symbol] = data
        
        symbols = list(all_assets.keys())
        
        for i, symbol_a in enumerate(symbols):
            for j, symbol_b in enumerate(symbols[i+1:], i+1):
                try:
                    # Use confluence vectors for correlation
                    vec_a = np.array(all_assets[symbol_a]['confluence_vector'])
                    vec_b = np.array(all_assets[symbol_b]['confluence_vector'])
                    
                    # Calculate cosine similarity
                    if np.linalg.norm(vec_a) > 0 and np.linalg.norm(vec_b) > 0:
                        correlation = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
                    else:
                        correlation = 0.0
                    
                    pair_key = f"{symbol_a}_{symbol_b}"
                    self.correlations[pair_key] = correlation
                    
                except Exception as e:
                    continue

    def save_processed_data(self, market_data: Dict):
        """Save all processed data for frontend consumption"""
        
        # Main market data file
        with open(os.path.join(self.data_dir, 'market_data.json'), 'w') as f:
            # Convert numpy arrays to lists for JSON serialization
            json_data = {}
            for asset_type, assets in market_data.items():
                json_data[asset_type] = {}
                for symbol, data in assets.items():
                    json_data[asset_type][symbol] = data.copy()
                    # Ensure confluence_vector is a list
                    if isinstance(json_data[asset_type][symbol]['confluence_vector'], np.ndarray):
                        json_data[asset_type][symbol]['confluence_vector'] = json_data[asset_type][symbol]['confluence_vector'].tolist()
            
            json.dump(json_data, f, indent=2, default=str)
        
        # Correlations file
        with open(os.path.join(self.data_dir, 'correlations.json'), 'w') as f:
            json.dump(self.correlations, f, indent=2)
        
        # Adaptive weights file
        with open(os.path.join(self.data_dir, 'adaptive_weights.json'), 'w') as f:
            json.dump(self.adaptive_weights, f, indent=2)
        
        # Create CSV for legacy compatibility
        self.create_csv_exports(market_data)

    def create_csv_exports(self, market_data: Dict):
        """Create CSV files for different use cases"""
        
        # Flattened data for general use
        flat_data = []
        for asset_type, assets in market_data.items():
            for symbol, data in assets.items():
                row = {
                    'symbol': symbol,
                    'asset_type': asset_type,
                    'current_price': data['current_price'],
                    'price_change_24h': data['price_change_24h'],
                    'volume': data['volume'],
                    'sentiment': data['sentiment'],
                    'entropy': data['entropy'],
                    'confluence_magnitude': data['confluence_magnitude'],
                    'last_updated': data['last_updated']
                }
                
                # Add indicator values
                for indicator, value in data['indicators'].items():
                    row[f'indicator_{indicator}'] = value
                
                flat_data.append(row)
        
        df_flat = pd.DataFrame(flat_data)
        df_flat.to_csv(os.path.join(self.data_dir, 'market_data_flat.csv'), index=False)
        
        # Correlations matrix
        if self.correlations:
            corr_data = []
            for pair, correlation in self.correlations.items():
                symbol_a, symbol_b = pair.split('_')
                corr_data.append({
                    'symbol_a': symbol_a,
                    'symbol_b': symbol_b,
                    'correlation': correlation
                })
            
            df_corr = pd.DataFrame(corr_data)
            df_corr.to_csv(os.path.join(self.data_dir, 'correlations.csv'), index=False)

    def generate_shape_mapping_data(self, market_data: Dict) -> Dict:
        """Generate 3D shape mapping data for visualization"""
        shape_data = {}
        
        for asset_type, assets in market_data.items():
            shape_data[asset_type] = {}
            
            for symbol, data in assets.items():
                # Map financial metrics to geometric properties
                confluence = data['confluence_magnitude']
                sentiment = data['sentiment']
                volatility = data['indicators'].get('volatility', 0.02)
                volume = data['volume']
                entropy = data['entropy']
                
                # Calculate shape properties
                shape_props = {
                    'position': {
                        'x': data['confluence_vector'][0] * 10,
                        'y': data['confluence_vector'][1] * 10,
                        'z': data['confluence_vector'][2] * 10
                    },
                    'scale': {
                        'base': max(0.5, confluence * 2),
                        'volatility_multiplier': 1 + volatility * 5
                    },
                    'color': {
                        'hue': 0.33 if sentiment > 0 else 0.0,  # Green for positive, red for negative
                        'saturation': min(abs(sentiment) + 0.3, 1.0),
                        'lightness': max(0.2, 0.8 - volatility * 2)
                    },
                    'animation': {
                        'pulse_frequency': max(0.1, 1.0 / (1 + abs(sentiment))),
                        'rotation_speed': entropy * 0.1,
                        'oscillation_amplitude': volatility * 0.5
                    },
                    'shape_type': self._determine_shape_type(data),
                    'metadata': {
                        'symbol': symbol,
                        'price': data['current_price'],
                        'change_24h': data['price_change_24h'],
                        'confluence': confluence,
                        'sentiment': sentiment,
                        'indicators': data['indicators']
                    }
                }
                
                shape_data[asset_type][symbol] = shape_props
        
        # Save shape mapping data
        with open(os.path.join(self.data_dir, 'shape_mapping.json'), 'w') as f:
            json.dump(shape_data, f, indent=2, default=str)
        
        return shape_data

    def _determine_shape_type(self, asset_data: Dict) -> str:
        """Determine 3D shape type based on market characteristics"""
        confluence = asset_data['confluence_magnitude']
        volatility = asset_data['indicators'].get('volatility', 0.02)
        rsi = asset_data['indicators'].get('rsi', 50)
        
        if confluence > 0.7:
            return 'icosahedron'  # High confluence = complex geometry
        elif volatility > 0.05:
            return 'octahedron'   # High volatility = sharp edges
        elif rsi > 70 or rsi < 30:
            return 'tetrahedron'  # Extreme RSI = pyramid warning
        else:
            return 'sphere'       # Default = simple sphere

def main():
    """Main execution function"""
    print("🚀 Starting Financial Market Engine 2.0...")
    
    # Initialize engine
    engine = FinancialMarketEngine(
        data_dir="data",
        news_api_key=os.getenv('NEWS_API_KEY')  # Set your NewsAPI key in environment
    )
    
    # Process all market data
    market_data = engine.process_all_assets()
    
    # Generate shape mapping for 3D visualization
    shape_data = engine.generate_shape_mapping_data(market_data)
    
    # Print summary
    total_assets = sum(len(assets) for assets in market_data.values())
    total_correlations = len(engine.correlations)
    
    print(f"\n📊 PROCESSING COMPLETE:")
    print(f"✅ Assets processed: {total_assets}")
    print(f"✅ Correlations calculated: {total_correlations}")
    print(f"✅ Shape mappings generated: {len(shape_data)}")
    print(f"✅ Data saved to: {engine.data_dir}/")
    
    print(f"\n📁 Generated Files:")
    print(f"- market_data.json (complete market data)")
    print(f"- correlations.json (asset correlations)")
    print(f"- adaptive_weights.json (ML weights)")
    print(f"- shape_mapping.json (3D visualization data)")
    print(f"- market_data_flat.csv (tabular export)")
    print(f"- correlations.csv (correlation matrix)")
    
    return market_data, shape_data

if __name__ == "__main__":
    main()
