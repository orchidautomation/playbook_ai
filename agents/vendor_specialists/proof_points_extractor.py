from agno.agent import Agent
import config
from models.vendor_elements import ProofPoint
from typing import List
from pydantic import BaseModel


class ProofPointsExtractionResult(BaseModel):
    proof_points: List[ProofPoint]


proof_points_extractor = Agent(
    name="Proof Points Extractor",
    model=config.EXTRACTION_MODEL,  # gpt-4o-mini for fast extraction
    description="Expert at identifying credibility indicators, social proof, testimonials, statistics, awards, and certifications from company content.",
    instructions=[
        "Extract ALL proof points including: Testimonials (customer quotes and endorsements), Statistics (usage stats, growth metrics), Awards (industry recognition, badges), and Certifications (compliance, security, industry standards).",
        "For each proof point, capture: Type (testimonial/statistic/award/certification), Content (actual proof point text), Source attribution (who said it or where from), and Sources (URLs with page_type).",
        "Look across all pages for credibility indicators: customer testimonials, 'Trusted by X companies' statements, industry awards, compliance badges (SOC2, GDPR, etc.), usage statistics, growth metrics, and customer satisfaction scores.",
        "Return comprehensive list of ALL proof points found.",
        "Capture exact wording and attribution when available.",
    ],
    output_schema=ProofPointsExtractionResult
)
