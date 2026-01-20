"""
Playbook AI - Configuration
Loads environment variables and defines workflow settings.
https://github.com/orchidautomation/playbook_ai-oss
"""

import os
from dotenv import load_dotenv
from agno.models.openai import OpenAIResponses

# Load environment variables from .env file
load_dotenv()

# API Keys
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Validate required keys
if not FIRECRAWL_API_KEY:
    raise ValueError("FIRECRAWL_API_KEY not found in environment variables")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Workflow Settings
MAX_URLS_TO_SCRAPE = int(os.getenv("MAX_URLS_TO_SCRAPE", "50"))  # 25 vendor + 25 prospect
BATCH_SCRAPE_TIMEOUT = int(os.getenv("BATCH_SCRAPE_TIMEOUT", "180"))  # 3 minutes
BATCH_SCRAPE_POLL_INTERVAL = 2  # Poll every 2 seconds

# Model Configuration (model-as-string format)
# Agno 2.2.6+ supports model-as-string format: "provider:model_id"
# See: https://docs.agno.com/concepts/models/model-as-string
#
# GPT-5.1 Configuration:
# - 400k context window, 128k max output tokens
# - Default reasoning effort: "none" (fastest, similar to gpt-4o)
# - TPM Tier 1: 500,000 tokens (16x higher than gpt-4o)
# - Supports structured outputs, function calling, tool use

# Primary models for different task types
# Note: gpt-5/gpt-5.1 require org verification - using gpt-4.1/gpt-4o as fallback
DEFAULT_MODEL = OpenAIResponses(id="gpt-4.1")           # Complex reasoning, synthesis, creative writing
FAST_MODEL = OpenAIResponses(id="gpt-4o-mini")          # Simple tasks, pattern matching (faster/cheaper)
REASONING_MODEL = OpenAIResponses(id="gpt-4.1")         # Analysis, complex reasoning tasks
EXTRACTION_MODEL = OpenAIResponses(id="gpt-4o-mini")    # Data extraction, entity extraction (cheaper)

# Legacy constant (kept for compatibility)
OPENAI_MODEL = "gpt-4o"

# Scraping Configuration
SCRAPE_WAIT_TIME = 2000  # Wait 2 seconds for page load (in milliseconds)
DEFAULT_SCRAPE_FORMATS = ['markdown', 'html']
BATCH_SCRAPE_FORMAT = ['markdown']  # Only markdown for batch to save tokens

# Scraping Performance - Use cached data for 500% faster scraping
SCRAPE_MAX_AGE = 172800000  # 48 hours in milliseconds (2 days)
                            # Firecrawl will use cached data if available
                            # Set to 0 to force fresh scrapes

# URL Mapping Configuration
MAX_URLS_TO_MAP = 5000  # Maximum URLs to discover per domain

# URL Prioritization Configuration
MAX_URLS_FOR_PRIORITIZATION = 200  # Maximum URLs to send to prioritization agent

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
