from agno.agent import Agent
import config
from models.vendor_elements import TargetPersona
from typing import List
from pydantic import BaseModel


class TargetPersonasExtractionResult(BaseModel):
    target_personas: List[TargetPersona]


persona_extractor = Agent(
    name="Vendor ICP Persona Extractor",
    model=config.EXTRACTION_MODEL,  # gpt-4o-mini for fast extraction
    description="Expert at identifying a vendor's ICP (Ideal Customer Profile) personas - the types of buyers they typically sell to.",
    instructions=[
        "IMPORTANT: Extract the types of buyers the VENDOR typically sells to. This is their target market profile, NOT specific personas at a particular prospect company.",
        "Extract ALL personas the vendor targets - who they typically sell to.",
        "For each persona, capture: Title (job title like 'CMO', 'VP Sales', 'Product Manager'), Department (function), Responsibilities (key responsibilities), Pain points (problems this persona faces), and Sources (URLs with page_type).",
        "Look for persona-specific landing pages, 'For [Role]' sections, testimonials with titles, use cases by role, product messaging by audience, and CTA language ('For marketing teams', etc.).",
        "Infer personas from: who testimonials are from, who use cases target, job titles in case studies, role-based messaging, and department-specific solutions.",
        "Examples of personas: Chief Marketing Officer (CMO), VP of Sales, Revenue Operations Manager, Product Manager, Customer Success Director.",
        "Extract both explicit personas (directly mentioned) and implicit personas (inferred from content).",
        "Remember: These are the vendor's TYPICAL buyer personas (their ICP), not specific people at a prospect company.",
    ],
    output_schema=TargetPersonasExtractionResult
)
