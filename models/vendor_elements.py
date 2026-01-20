from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from models.common import Source


class Offering(BaseModel):
    """Product or service offering"""
    name: str = Field(description="Name of the product or service offering")
    description: str = Field(description="Detailed description of what the offering provides")
    features: List[str] = Field(default_factory=list, description="List of key features included in this offering")
    pricing_indicators: Optional[str] = Field(default=None, description="Pricing information or pricing tier indicators")
    target_audience: Optional[str] = Field(default=None, description="Primary audience or market segment for this offering")
    sources: List[Source] = Field(default_factory=list, description="Sources where this offering information was found")


class CaseStudy(BaseModel):
    """Customer success story"""
    customer_name: str = Field(description="Name of the customer featured in the case study")
    industry: Optional[str] = Field(default=None, description="Industry vertical of the customer")
    company_size: Optional[str] = Field(default=None, description="Size of the customer company (e.g., SMB, Enterprise, employee count)")
    challenge: str = Field(description="Business challenge or problem the customer faced")
    solution: str = Field(description="How the vendor's product/service addressed the challenge")
    results: List[str] = Field(default_factory=list, description="Outcomes and results achieved by the customer")
    metrics: List[str] = Field(default_factory=list, description="Quantifiable metrics demonstrating success (e.g., ROI, time saved)")
    sources: List[Source] = Field(default_factory=list, description="Sources where this case study was found")


class ProofPoint(BaseModel):
    """Testimonial, stat, or credibility indicator"""
    type: Literal["testimonial", "statistic", "award", "certification"] = Field(
        description="Type of proof point: testimonial, statistic, award, or certification"
    )
    content: str = Field(description="The actual proof point content (quote, stat, award name, etc.)")
    source_attribution: Optional[str] = Field(default=None, description="Attribution for the proof point (person name, organization, etc.)")
    sources: List[Source] = Field(default_factory=list, description="Sources where this proof point was found")


class ValueProposition(BaseModel):
    """Core value proposition"""
    statement: str = Field(description="The core value proposition statement")
    benefits: List[str] = Field(default_factory=list, description="List of benefits supporting the value proposition")
    differentiation: Optional[str] = Field(default=None, description="How this value proposition differentiates from competitors")
    target_persona: Optional[str] = Field(default=None, description="The persona or role this value proposition resonates with most")
    sources: List[Source] = Field(default_factory=list, description="Sources where this value proposition was found")


class ReferenceCustomer(BaseModel):
    """Customer reference"""
    name: str = Field(description="Name of the reference customer or partner")
    logo_url: Optional[str] = Field(default=None, description="URL to the customer's logo image")
    industry: Optional[str] = Field(default=None, description="Industry vertical of the customer")
    company_size: Optional[str] = Field(default=None, description="Size of the customer company (e.g., SMB, Enterprise, employee count)")
    relationship: Literal["customer", "partner", "integration"] = Field(
        description="Type of relationship: customer, partner, or integration"
    )
    sources: List[Source] = Field(default_factory=list, description="Sources where this reference was found")


class UseCase(BaseModel):
    """Use case or workflow solution"""
    title: str = Field(description="Title or name of the use case")
    description: str = Field(description="Detailed description of the use case and how it works")
    target_persona: Optional[str] = Field(default=None, description="The persona or role this use case is designed for")
    target_industry: Optional[str] = Field(default=None, description="Industry vertical this use case is most relevant to")
    problems_solved: List[str] = Field(default_factory=list, description="List of problems or pain points this use case addresses")
    key_features_used: List[str] = Field(default_factory=list, description="Key product features utilized in this use case")
    sources: List[Source] = Field(default_factory=list, description="Sources where this use case was found")


class TargetPersona(BaseModel):
    """
    Vendor's ICP (Ideal Customer Profile) Persona

    This represents the types of buyers the vendor TYPICALLY sells to,
    not specific personas at a particular prospect company.
    Used to understand vendor's go-to-market focus and typical buyer profiles.
    """
    title: str = Field(description="Job title or role of the target persona")
    department: Optional[str] = Field(default=None, description="Department or functional area the persona belongs to")
    responsibilities: List[str] = Field(default_factory=list, description="Key responsibilities and duties of this persona")
    pain_points: List[str] = Field(default_factory=list, description="Common pain points and challenges faced by this persona")
    sources: List[Source] = Field(default_factory=list, description="Sources where this persona information was found")


class Differentiator(BaseModel):
    """Competitive differentiator"""
    category: Literal["feature", "approach", "market_position", "technology"] = Field(
        description="Category of differentiation: feature, approach, market_position, or technology"
    )
    statement: str = Field(description="The differentiating statement or claim")
    vs_alternative: Optional[str] = Field(default=None, description="What alternative or competitor this differentiates against")
    evidence: List[str] = Field(default_factory=list, description="Evidence or proof points supporting this differentiator")
    sources: List[Source] = Field(default_factory=list, description="Sources where this differentiator was found")


class VendorElements(BaseModel):
    """Complete vendor GTM element library"""
    offerings: List[Offering] = Field(default_factory=list, description="Product and service offerings from the vendor")
    case_studies: List[CaseStudy] = Field(default_factory=list, description="Customer success stories and case studies")
    proof_points: List[ProofPoint] = Field(default_factory=list, description="Testimonials, statistics, awards, and certifications")
    value_propositions: List[ValueProposition] = Field(default_factory=list, description="Core value propositions and messaging")
    reference_customers: List[ReferenceCustomer] = Field(default_factory=list, description="Customer references and logos")
    use_cases: List[UseCase] = Field(default_factory=list, description="Use cases and workflow solutions")
    vendor_icp_personas: List[TargetPersona] = Field(
        default_factory=list,
        description="Vendor's ICP - types of buyers they typically sell to (not prospect-specific)"
    )
    differentiators: List[Differentiator] = Field(default_factory=list, description="Competitive differentiators and unique selling points")
