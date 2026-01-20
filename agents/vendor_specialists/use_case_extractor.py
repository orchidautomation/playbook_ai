from agno.agent import Agent
import config
from models.vendor_elements import UseCase
from typing import List
from pydantic import BaseModel


class UseCasesExtractionResult(BaseModel):
    use_cases: List[UseCase]


use_case_extractor = Agent(
    name="Use Case Extractor",
    model=config.EXTRACTION_MODEL,  # gpt-4o-mini for fast extraction
    description="Expert at identifying use cases, workflow solutions, and specific ways customers use B2B products.",
    instructions=[
        "Extract ALL use cases - specific ways customers use the product.",
        "For each use case, capture: Title (name), Description (what it accomplishes), Target persona (who uses it), Target industry (industry focus), Problems solved (list of problems addressed), Key features used, and Sources (URLs with page_type).",
        "Look for /use-cases pages, /solutions pages, /industries pages, workflow descriptions, 'How to' sections, problem-solution narratives, and industry-specific solutions.",
        "Capture both broad and specific use cases. Examples: 'Lead qualification automation', 'Customer onboarding workflows', 'Sales forecasting', 'Marketing campaign attribution'.",
        "For each use case, identify: what workflow/process it addresses, what problem it solves, who typically uses it, and what product features enable it.",
    ],
    output_schema=UseCasesExtractionResult
)
