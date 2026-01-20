from agno.agent import Agent
import config
from models.vendor_elements import Differentiator
from typing import List
from pydantic import BaseModel


class DifferentiatorsExtractionResult(BaseModel):
    differentiators: List[Differentiator]


differentiator_extractor = Agent(
    name="Competitive Differentiator Extractor",
    model=config.EXTRACTION_MODEL,  # gpt-4o-mini for fast extraction
    description="Expert at identifying competitive differentiation, unique positioning, and what makes vendors stand out from alternatives.",
    instructions=[
        "Extract statements about what makes the vendor unique or better than alternatives.",
        "For each differentiator, capture: Category (feature/approach/market_position/technology), Statement (the differentiation claim), vs_alternative (what they're comparing against), Evidence (supporting proof), and Sources (URLs with page_type).",
        "Look for: 'Unlike other solutions...', 'The only platform that...', 'First to market...', unique feature claims, proprietary technology mentions, market positioning statements, competitive comparisons, and 'Why choose us' sections.",
        "Categories: 'feature' (unique product capabilities), 'approach' (unique methodology), 'market_position' (market leadership, first-mover, niche focus), 'technology' (proprietary tech, patents, unique architecture).",
        "Capture both explicit comparisons and implied differentiation.",
        "Examples: 'The only AI-powered platform with real-time sync', 'Unlike traditional CRMs, we use a revenue-first approach', 'Industry leader with 10+ years of expertise', 'Proprietary machine learning algorithms'.",
        "Extract evidence when available (customer proof, metrics, third-party validation).",
    ],
    output_schema=DifferentiatorsExtractionResult
)
