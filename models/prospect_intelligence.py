from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from models.common import Source


class CompanyProfile(BaseModel):
    """Minimal company context for sales intelligence"""
    company_name: str = Field(description="The official name of the prospect company")
    industry: Optional[str] = Field(default=None, description="The industry or sector the company operates in")
    company_size: Optional[str] = Field(default=None, description="SMB, Mid-market, Enterprise, or employee count range")
    what_they_do: str = Field(description="1-2 sentence description of their business")
    target_market: Optional[str] = Field(default=None, description="Who they sell to - industries, company types")
    sources: List[Source] = Field(default_factory=list, description="Sources used to gather company profile information")


class PainPoint(BaseModel):
    """Identified pain point or challenge (inferred from their content)"""
    description: str = Field(description="The pain point or challenge")
    category: Literal["operational", "strategic", "technical", "market", "growth"] = Field(
        description="Category of pain point: operational, strategic, technical, market, or growth"
    )
    evidence: str = Field(description="Why we think this is a pain point - what in their content suggests this")
    affected_personas: List[str] = Field(default_factory=list, description="Which roles likely feel this pain (job titles)")
    confidence: Literal["high", "medium", "low"] = Field(
        description="Confidence level: high (explicit mention), medium (implied), low (inferred from industry)"
    )
    sources: List[Source] = Field(default_factory=list, description="Sources used to identify this pain point")


class TargetBuyerPersona(BaseModel):
    """Buyer persona at prospect that vendor should target for outreach"""
    persona_title: str = Field(description="Job title or role (e.g., VP Sales, CMO, Head of Revenue Ops)")
    department: str = Field(description="Department or function (Sales, Marketing, Revenue Ops, etc.)")
    why_they_care: str = Field(description="Why this persona would care about vendor's solution - their motivation")
    pain_points: List[str] = Field(default_factory=list, description="Specific pain points this role faces")
    goals: List[str] = Field(default_factory=list, description="What this persona is trying to achieve")
    suggested_talking_points: List[str] = Field(default_factory=list, description="How to connect vendor solution to their needs")
    priority_score: int = Field(ge=1, le=10, description="1-10 priority score for targeting this persona (10 = highest priority)")
    sources: List[Source] = Field(default_factory=list, description="Sources used to build this persona profile")


class ProspectIntelligence(BaseModel):
    """Complete prospect intelligence package - streamlined for sales outreach"""
    company_profile: CompanyProfile = Field(description="Core company information and context")
    pain_points: List[PainPoint] = Field(default_factory=list, description="Company/role-level pain points identified")
    target_buyer_personas: List[TargetBuyerPersona] = Field(default_factory=list, description="3-5 key personas vendor should target")
