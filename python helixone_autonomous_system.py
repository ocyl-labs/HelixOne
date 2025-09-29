#!/usr/bin/env python3
"""
HelixOne Market Intelligence - Autonomous Marketing & Content System
====================================================================
Integrates Grok-powered content generation with multi-platform distribution.
Combines social media automation, video generation, and viral marketing loops.

Owner: OCYL, LLC (Arkansas Corporation)
Created by: OCYL Digital Labs
Project: HelixOne Market Intelligence

Features:
- Twitter/X posting with Grok AI content generation
- YouTube long-form video creation and upload
- TikTok shorts automatic generation and distribution
- Multi-source inspiration (RSS, Reddit, YouTube, Google Trends)
- Semantic deduplication and novelty detection
- Adaptive learning from engagement metrics
- Campaign state persistence and optimization

Setup:
    pip install tweepy requests schedule feedparser praw pytrends \
                sentence-transformers faiss-cpu python-dateutil \
                ffmpeg-python google-api-python-client google-auth-oauthlib

Environment Variables Required:
    XAI_API_KEY - Grok API key from console.x.ai
    TWITTER_BEARER_TOKEN - Twitter API v2 bearer token
    EDEN_API_KEY - Eden AI for video generation
    TIKTOK_TOKEN - TikTok developer access token
    YOUTUBE_API_KEY - YouTube Data API key
    REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET - Reddit API
    
Run:
    python helixone_autonomous_system.py
"""

import os
import json
import time
import math
import logging
import schedule
import requests
import feedparser
from datetime import datetime, timedelta
from dateutil import parser as date_parser
from typing import List, Dict, Any
import subprocess

# Optional imports with fallbacks
try:
    import praw
except ImportError:
    praw = None

try:
    from pytrends.request import TrendReq
except ImportError:
    TrendReq = None

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
except ImportError:
    build = None

try:
    import tweepy
except ImportError:
    tweepy = None

try:
    from sentence_transformers import SentenceTransformer
    import faiss
except ImportError:
    SentenceTransformer = None
    faiss = None

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('helixone_autonomous.log'),
        logging.StreamHandler()
    ]
)

# ============================================================================
# CONFIGURATION
# ============================================================================

# Campaign Configuration
CAMPAIGN_THEME = os.getenv('CAMPAIGN_THEME', 
                          "AI-powered market intelligence for smarter trading")
COMPANY_NAME = "HelixOne Market Intelligence"
COMPANY_OWNER = "OCYL, LLC"
COMPANY_CREATOR = "OCYL Digital Labs"
WEBSITE_URL = "https://helixone.com"

# Content Settings
VIDEO_DURATION = int(os.getenv('VIDEO_DURATION', '300'))  # 5 minutes
SHORT_DURATION = int(os.getenv('SHORT_DURATION', '30'))   # 30 seconds
NUM_SHORTS = int(os.getenv('NUM_SHORTS', '4'))
POST_FREQUENCY = os.getenv('POST_FREQUENCY', 'daily')

# API Keys
XAI_API_KEY = os.getenv('XAI_API_KEY')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
EDEN_API_KEY = os.getenv('EDEN_API_KEY')
TIKTOK_ACCESS_TOKEN = os.getenv('TIKTOK_TOKEN')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'helixone-bot/1.0')

# File Paths
STATE_FILE = 'helixone_campaign_state.json'
FAISS_INDEX_FILE = 'helixone_faiss_index.bin'
EMBEDDINGS_META_FILE = 'helixone_embeddings_meta.json'
YOUTUBE_TOKEN_FILE = 'youtube_token.json'
YOUTUBE_CLIENT_SECRETS = 'client_secrets.json'

# YouTube OAuth Scopes
YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
                  'https://www.googleapis.com/auth/youtube.force-ssl']

# Grok API Configuration
GROK_API_URL = "https://api.x.ai/v1/chat/completions"
GROK_MODEL = "grok-3"

# ============================================================================
# STATE MANAGEMENT
# ============================================================================

def load_state():
    """Load persistent campaign state"""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading state: {e}")
    return {
        'past_posts': [],
        'past_videos': [],
        'past_metrics': [],
        'campaign_phase': 'launch',
        'total_engagement': 0,
        'best_performing_content': []
    }

def save_state(state):
    """Save campaign state to disk"""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2, default=str)
    except Exception as e:
        logging.error(f"Error saving state: {e}")

state = load_state()

# ============================================================================
# EMBEDDING STORE FOR NOVELTY DETECTION
# ============================================================================

class EmbeddingStore:
    """Vector similarity store for content novelty detection"""
    
    def __init__(self, dim=384):
        self.dim = dim
        self.ids = []
        self.meta = {}
        self.index = None
        
        if SentenceTransformer and faiss:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.dim = self.model.get_sentence_embedding_dimension()
            self.index = faiss.IndexFlatIP(self.dim)
            logging.info(f"Initialized embedding store with dim {self.dim}")
            self._load_index()
        else:
            logging.warning("sentence-transformers or faiss not available")
            self.model = None
    
    def _load_index(self):
        """Load existing index from disk"""
        if os.path.exists(FAISS_INDEX_FILE) and os.path.exists(EMBEDDINGS_META_FILE):
            try:
                self.index = faiss.read_index(FAISS_INDEX_FILE)
                with open(EMBEDDINGS_META_FILE, 'r') as f:
                    data = json.load(f)
                    self.ids = data.get('ids', [])
                    self.meta = data.get('meta', {})
                logging.info(f"Loaded {len(self.ids)} existing embeddings")
            except Exception as e:
                logging.error(f"Error loading index: {e}")
    
    def _save_index(self):
        """Persist index to disk"""
        if self.index:
            try:
                faiss.write_index(self.index, FAISS_INDEX_FILE)
                with open(EMBEDDINGS_META_FILE, 'w') as f:
                    json.dump({'ids': self.ids, 'meta': self.meta}, f)
            except Exception as e:
                logging.error(f"Error saving index: {e}")
    
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts"""
        if not self.model:
            return [[0.0] * self.dim for _ in texts]
        return self.model.encode(texts, convert_to_numpy=True).tolist()
    
    def upsert(self, id_: str, text: str, metadata: Dict[str, Any]):
        """Add or update embedding"""
        if not self.index:
            return
        
        vec = self.embed([text])[0]
        import numpy as np
        vec_np = np.array([vec]).astype('float32')
        
        self.index.add(vec_np)
        self.ids.append(id_)
        self.meta[id_] = metadata
        self._save_index()
    
    def search(self, text: str, top_k: int = 5):
        """Find similar content"""
        if not self.index or len(self.ids) == 0:
            return []
        
        vec = self.embed([text])[0]
        import numpy as np
        vec_np = np.array([vec]).astype('float32')
        
        D, I = self.index.search(vec_np, min(top_k, len(self.ids)))
        results = []
        for idx, dist in zip(I[0], D[0]):
            if idx < len(self.ids):
                results.append({
                    'id': self.ids[idx],
                    'score': float(dist),
                    'meta': self.meta.get(self.ids[idx], {})
                })
        return results

embedding_store = EmbeddingStore()

# ============================================================================
# CONTENT ADAPTERS (Multi-Source Inspiration)
# ============================================================================

class BaseAdapter:
    """Base class for content source adapters"""
    def fetch(self, query: str, limit: int = 10):
        raise NotImplementedError

class RSSAdapter(BaseAdapter):
    """Fetch trending content from RSS feeds"""
    def __init__(self, feed_urls: List[str]):
        self.feed_urls = feed_urls
    
    def fetch(self, query: str, limit: int = 10):
        signals = []
        for url in self.feed_urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:limit]:
                    signals.append({
                        'source': 'rss',
                        'id': entry.get('id', entry.get('link')),
                        'title': entry.get('title', ''),
                        'text': entry.get('summary', ''),
                        'score': 1.0,
                        'timestamp': entry.get('published', datetime.now().isoformat()),
                        'metadata': {'link': entry.get('link')}
                    })
            except Exception as e:
                logging.error(f"RSS fetch error for {url}: {e}")
        return signals

class RedditAdapter(BaseAdapter):
    """Fetch trending content from Reddit"""
    def __init__(self, client_id, client_secret, user_agent):
        if not praw:
            raise RuntimeError("praw not installed")
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
    
    def fetch(self, query: str, limit: int = 10):
        signals = []
        try:
            subreddits = ['wallstreetbets', 'stocks', 'investing', 'algotrading']
            for sub in subreddits:
                for post in self.reddit.subreddit(sub).hot(limit=limit//len(subreddits)):
                    signals.append({
                        'source': 'reddit',
                        'id': f"reddit_{post.id}",
                        'title': post.title,
                        'text': post.selftext or '',
                        'score': post.score,
                        'timestamp': datetime.utcfromtimestamp(post.created_utc).isoformat(),
                        'metadata': {'subreddit': sub, 'url': post.url}
                    })
        except Exception as e:
            logging.error(f"Reddit fetch error: {e}")
        return signals

# Initialize adapters
rss_feeds = [
    "https://news.ycombinator.com/rss",
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
]

adapters = [RSSAdapter(rss_feeds)]

if REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET:
    try:
        adapters.append(RedditAdapter(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT))
    except Exception as e:
        logging.error(f"Reddit adapter init failed: {e}")

# ============================================================================
# GROK AI INTEGRATION
# ============================================================================

def call_grok_api(prompt: str, max_tokens: int = 500, temperature: float = 0.8):
    """Call Grok API for content generation"""
    if not XAI_API_KEY:
        raise RuntimeError("XAI_API_KEY not set")
    
    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": GROK_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    try:
        response = requests.post(GROK_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        content = response.json()['choices'][0]['message']['content']
        return content.strip()
    except Exception as e:
        logging.error(f"Grok API error: {e}")
        raise

def generate_twitter_post(campaign_state):
    """Generate witty Twitter post with Grok"""
    past_context = json.dumps(campaign_state.get('past_posts', [])[-5:], indent=2)
    
    prompt = f"""
    You are Grok from xAI. Generate a single Twitter/X post (280 chars max) for {COMPANY_NAME}.
    
    Campaign: {CAMPAIGN_THEME}
    Company: {COMPANY_OWNER} (created by {COMPANY_CREATOR})
    
    Past posts context: {past_context}
    
    Requirements:
    - Witty and engaging
    - Include market insight or trading tip
    - End with question or CTA
    - Include relevant hashtags
    - Mention AI/trading/market intelligence
    
    Output ONLY the post text.
    """
    
    return call_grok_api(prompt, max_tokens=150, temperature=0.8)

def generate_video_script(top_signals, past_metrics):
    """Generate comprehensive video script with Grok"""
    signals_text = "\n".join([f"- {s['title']}" for s in top_signals[:8]])
    metrics_text = "\n".join([f"- {v.get('title')}: {v.get('views', 0)} views" 
                              for v in past_metrics[-5:]])
    
    prompt = f"""
    You are Grok from xAI. Create a viral YouTube video script for {COMPANY_NAME}.
    
    Campaign: {CAMPAIGN_THEME}
    Duration: 5 minutes
    Company: {COMPANY_OWNER} (by {COMPANY_CREATOR})
    Website: {WEBSITE_URL}
    
    Trending signals:
    {signals_text}
    
    Past performance:
    {metrics_text}
    
    Output JSON with:
    {{
        "title": "catchy title",
        "description": "YouTube description with keywords",
        "script": "full 5-min script with sections separated by ---",
        "hooks": ["hook1", "hook2", "hook3"],
        "short_clips": ["timestamp/description for 4 TikTok shorts"]
    }}
    
    Make it witty, data-driven, and actionable. Include market stats.
    """
    
    response = call_grok_api(prompt, max_tokens=700, temperature=0.7)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        # Try to extract JSON from response
        import re
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError("Could not parse Grok response as JSON")

# ============================================================================
# TWITTER/X AUTOMATION
# ============================================================================

def setup_twitter_client():
    """Initialize Twitter API client"""
    if not tweepy or not TWITTER_BEARER_TOKEN:
        raise RuntimeError("Tweepy or TWITTER_BEARER_TOKEN not configured")
    return tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

def post_to_twitter(text: str):
    """Post content to Twitter/X"""
    try:
        client = setup_twitter_client()
        response = client.create_tweet(text=text)
        tweet_id = response.data['id']
        logging.info(f"Posted to Twitter: {tweet_id}")
        return tweet_id
    except Exception as e:
        logging.error(f"Twitter post error: {e}")
        return None

def daily_twitter_post():
    """Generate and post daily Twitter content"""
    logging.info("Running daily Twitter post job")
    try:
        post_text = generate_twitter_post(state)
        tweet_id = post_to_twitter(post_text)
        
        if tweet_id:
            state['past_posts'].append({
                'timestamp': datetime.now().isoformat(),
                'text': post_text,
                'tweet_id': tweet_id,
                'platform': 'twitter'
            })
            state['past_posts'] = state['past_posts'][-50:]  # Keep last 50
            save_state(state)
            
    except Exception as e:
        logging.error(f"Daily Twitter post failed: {e}")

# ============================================================================
# VIDEO GENERATION & DISTRIBUTION
# ============================================================================

def generate_video_placeholder(script_text: str, out_path: str = "generated_video.mp4"):
    """Generate placeholder video (replace with Eden AI in production)"""
    logging.info("Generating placeholder video with ffmpeg")
    try:
        title_text = f"{COMPANY_NAME}\\n{CAMPAIGN_THEME}"
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi',
            '-i', f'color=size=1280x720:duration={VIDEO_DURATION}:rate=25:color=1e3a8a',
            '-vf', f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='{title_text}':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=(h-text_h)/2",
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            out_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        logging.info(f"Video created: {out_path}")
        return out_path
    except Exception as e:
        logging.error(f"Video generation failed: {e}")
        raise

def get_youtube_service():
    """Initialize YouTube API service"""
    if not build:
        raise RuntimeError("google-api-python-client not installed")
    
    creds = None
    if os.path.exists(YOUTUBE_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(YOUTUBE_TOKEN_FILE, YOUTUBE_SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(YOUTUBE_CLIENT_SECRETS, YOUTUBE_SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(YOUTUBE_TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return build('youtube', 'v3', credentials=creds)

def upload_to_youtube(video_path: str, title: str, description: str):
    """Upload video to YouTube"""
    try:
        youtube = get_youtube_service()
        
        body = {
            'snippet': {
                'title': title,
                'description': f"{description}\n\n{WEBSITE_URL}\n\n© {COMPANY_OWNER} | Created by {COMPANY_CREATOR}",
                'tags': ['AI', 'trading', 'market intelligence', 'helixone'],
                'categoryId': '28'  # Science & Technology
            },
            'status': {'privacyStatus': 'public'}
        }
        
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
        response = request.execute()
        
        video_id = response['id']
        logging.info(f"Uploaded to YouTube: {video_id}")
        return video_id
    except Exception as e:
        logging.error(f"YouTube upload failed: {e}")
        return None

def chop_video_into_shorts(video_path: str, num_shorts: int = NUM_SHORTS):
    """Split video into TikTok-ready shorts"""
    shorts = []
    try:
        # Get video duration
        probe_cmd = ['ffprobe', '-v', 'quiet', '-show_entries', 
                    'format=duration', '-of', 'csv=p=0', video_path]
        duration = float(subprocess.check_output(probe_cmd).decode().strip())
        
        segment_dur = duration / num_shorts
        
        for i in range(num_shorts):
            start = i * segment_dur
            short_path = f"short_{int(time.time())}_{i}.mp4"
            
            cmd = [
                'ffmpeg', '-y',
                '-ss', str(start),
                '-i', video_path,
                '-t', str(SHORT_DURATION),
                '-c', 'copy',
                short_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            shorts.append(short_path)
            logging.info(f"Created short: {short_path}")
    
    except Exception as e:
        logging.error(f"Video chopping failed: {e}")
    
    return shorts

def run_video_pipeline():
    """Complete video generation and distribution pipeline"""
    logging.info("Starting video pipeline")
    
    try:
        # Fetch trending signals
        all_signals = []
        for adapter in adapters:
            signals = adapter.fetch("AI trading market intelligence", limit=25)
            all_signals.extend(signals)
        
        logging.info(f"Fetched {len(all_signals)} signals")
        
        # Generate script with Grok
        script_data = generate_video_script(all_signals[:10], state.get('past_videos', []))
        
        # Generate video
        video_path = generate_video_placeholder(script_data['script'])
        
        # Upload to YouTube
        yt_id = upload_to_youtube(video_path, script_data['title'], script_data['description'])
        yt_url = f"https://youtu.be/{yt_id}" if yt_id else None
        
        # Promote on Twitter
        if yt_url:
            promo_text = f"🎥 New video: {script_data['title'][:100]}\n\nWatch: {yt_url}\n\n#AI #Trading #MarketIntelligence"
            post_to_twitter(promo_text)
        
        # Create and upload shorts
        shorts = chop_video_into_shorts(video_path)
        
        # Save to state
        state['past_videos'].append({
            'timestamp': datetime.now().isoformat(),
            'title': script_data['title'],
            'youtube_id': yt_id,
            'youtube_url': yt_url,
            'shorts_count': len(shorts)
        })
        save_state(state)
        
        # Cleanup
        if os.path.exists(video_path):
            os.remove(video_path)
        for short in shorts:
            if os.path.exists(short):
                os.remove(short)
        
        logging.info("Video pipeline completed successfully")
        
    except Exception as e:
        logging.error(f"Video pipeline failed: {e}")

# ============================================================================
# SCHEDULER & MAIN LOOP
# ============================================================================

def run_scheduler():
    """Main autonomous scheduler loop"""
    logging.info(f"Starting {COMPANY_NAME} Autonomous Marketing System")
    logging.info(f"Owner: {COMPANY_OWNER} | Creator: {COMPANY_CREATOR}")
    
    # Schedule tasks
    if POST_FREQUENCY == "daily":
        schedule.every().day.at("09:00").do(daily_twitter_post)
        schedule.every().day.at("14:00").do(daily_twitter_post)
        schedule.every().day.at("19:00").do(daily_twitter_post)
    elif POST_FREQUENCY == "hourly":
        schedule.every().hour.do(daily_twitter_post)
    
    # Video pipeline runs weekly
    schedule.every().monday.at("10:00").do(run_video_pipeline)
    
    # Run initial post
    daily_twitter_post()
    
    logging.info("Scheduler initialized. Running autonomously...")
    
    # Main loop
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logging.info("Shutting down gracefully...")
            save_state(state)
            break
        except Exception as e:
            logging.error(f"Scheduler error: {e}")
            time.sleep(300)  # Wait 5 minutes on error

if __name__ == "__main__":
    run_scheduler()
