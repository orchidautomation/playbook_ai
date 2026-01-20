from agno.agent import Agent
import config
from models.vendor_elements import Offering
from typing import List
from pydantic import BaseModel


class OfferingsExtractionResult(BaseModel):
    offerings: List[Offering]


offerings_extractor = Agent(
    name="Offerings Extractor",
    model=config.EXTRACTION_MODEL,  # gpt-4o-mini for fast extraction
    description="Expert at identifying and cataloging product offerings, services, and platform components from B2B company content.",
    instructions=[
        "Extract ALL products, services, or platform components mentioned in the content.",
        "For each offering, extract: Name (official product/service name), Description (what it does in 1-2 sentences), Features (list of key capabilities), Pricing indicators (free tier, enterprise, etc.), Target audience (who it's for), and Sources (URLs with page_type).",
        "Look for product pages (/products, /platform, /solutions), feature lists, pricing pages, homepage offerings, and service descriptions.",
        "Return comprehensive structured output with ALL offerings found.",
        "Be thorough - capture every distinct product or service offering.",
    ],
    output_schema=OfferingsExtractionResult
)
