from agno.agent import Agent
import config
from models.vendor_elements import CaseStudy
from typing import List
from pydantic import BaseModel


class CaseStudiesExtractionResult(BaseModel):
    case_studies: List[CaseStudy]


case_study_extractor = Agent(
    name="Case Study Extractor",
    model=config.EXTRACTION_MODEL,  # gpt-4o-mini for fast extraction
    description="Expert at extracting customer success stories, case studies, and detailed success narratives from B2B company websites.",
    instructions=[
        "Extract ALL case studies, customer stories, and success examples from the provided content.",
        "For each case study, extract: Customer name, Industry, Company size (SMB/Mid-market/Enterprise), Challenge (problem faced), Solution (how vendor helped), Results (outcomes achieved), Metrics (quantified results like %, $, time saved), and Sources (URLs with page_type).",
        "Look for /customers, /case-studies, /success-stories pages, customer testimonials with details, homepage customer highlights, and detailed success narratives.",
        "Return all case studies found with complete details.",
        "Extract metrics whenever available - numbers matter for sales intelligence.",
    ],
    output_schema=CaseStudiesExtractionResult
)
