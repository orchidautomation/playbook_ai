from agno.agent import Agent
import config
from models.vendor_elements import ReferenceCustomer
from typing import List
from pydantic import BaseModel


class ReferenceCustomersExtractionResult(BaseModel):
    reference_customers: List[ReferenceCustomer]


customer_extractor = Agent(
    name="Reference Customer Extractor",
    model=config.EXTRACTION_MODEL,  # gpt-4o-mini for fast extraction
    description="Expert at identifying customer references, logos, and company mentions from B2B websites for sales intelligence.",
    instructions=[
        "Extract ALL customer references, logos, and company mentions from the content.",
        "For each reference, capture: Name (company name), Logo URL (if visible), Industry (if mentioned or inferable), Company size (SMB/Mid-market/Enterprise), Relationship (customer/partner/integration/other), and Sources (URLs with page_type).",
        "Look for customer logo walls, 'Trusted by' sections, partner pages, integration pages, case study customer names, testimonial attributions, and customer listings.",
        "Capture ALL companies mentioned, even if minimal info available.",
        "Relationship types: 'customer' (paying customer), 'partner' (business partner/reseller), 'integration' (technology integration partner), 'other' (unknown relationship).",
        "Extract company size indicators like Fortune 500, Enterprise, SMB, Mid-market, or employee count if mentioned.",
    ],
    output_schema=ReferenceCustomersExtractionResult
)
