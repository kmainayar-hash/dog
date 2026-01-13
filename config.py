"""
Configuration settings for Dog Influencer Scraper
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Scraper settings
SCRAPER_MODE = os.getenv("SCRAPER_MODE", "demo")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "dog_influencers_by_state.json")

# Rate limiting
MIN_DELAY = float(os.getenv("MIN_DELAY", "2"))
MAX_DELAY = float(os.getenv("MAX_DELAY", "5"))

# API Keys (for future use)
INSTAGRAM_API_KEY = os.getenv("INSTAGRAM_API_KEY", "")
TIKTOK_API_KEY = os.getenv("TIKTOK_API_KEY", "")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

# User agent rotation
USE_RANDOM_USER_AGENT = True

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
