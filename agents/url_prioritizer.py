"""
URL Prioritizer Agent
Selects the most valuable pages from vendor and prospect websites for intelligence gathering.
Uses OpenAI GPT-4o-mini for fast URL filtering (40-60% faster than gpt-4o).
"""

from agno.agent import Agent
from pydantic import BaseModel, Field
from typing import List
import config


class PrioritizedURL(BaseModel):
    """Single prioritized URL with metadata"""
    url: str
    page_type: str = Field(description="e.g., 'about', 'case_study', 'pricing', 'blog'")
    priority: int = Field(description="1 (highest) to 10 (lowest)")
    reasoning: str


class URLPrioritizationResult(BaseModel):
    """Result containing prioritized URLs for both vendor and prospect"""
    vendor_selected_urls: List[PrioritizedURL]
    prospect_selected_urls: List[PrioritizedURL]


url_prioritizer = Agent(
    name="Strategic URL Selector",
    model=config.FAST_MODEL,  # gpt-4o-mini: 40-60% faster!
    description="Content strategist selecting the most valuable pages from vendor and prospect websites for B2B sales intelligence gathering.",
    instructions=[
        "Given lists of URLs from vendor and prospect websites, select the TOP 10-15 MOST VALUABLE pages for each.",
        "PRIORITIZE: /about, /about-us, /company, /team, /leadership pages.",
        "PRIORITIZE: /products, /solutions, /platform, /features pages.",
        "PRIORITIZE: /customers, /case-studies, /success-stories, /testimonials pages.",
        "PRIORITIZE: /pricing, /plans pages.",
        "PRIORITIZE: /blog (recent posts with dates in URL), /industries, /use-cases, /resources pages.",
        "AVOID: Legal pages (/privacy, /terms, /legal, /cookies).",
        "AVOID: Career pages (/careers, /jobs, /join-us).",
        "AVOID: Support docs (/help, /docs, /support, /faq).",
        "AVOID: Login/signup pages (/login, /signup, /register).",
        "AVOID: Media/press pages (unless highly relevant).",
        "For each selected URL, provide: page_type (category), priority (1=must have to 10=nice to have), and reasoning (why valuable for sales intelligence).",
        "Return top 10-15 URLs per company, prioritized.",
    ],
    output_schema=URLPrioritizationResult
)
