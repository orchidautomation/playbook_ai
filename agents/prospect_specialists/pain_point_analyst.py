from agno.agent import Agent
from agno.models.openai import OpenAIChat
from models.prospect_intelligence import PainPoint
from typing import List
from pydantic import BaseModel


class PainPointsResult(BaseModel):
    pain_points: List[PainPoint]


pain_point_analyst = Agent(
    name="Pain Point Analyst",
    model=OpenAIChat(id="gpt-4o"),
    instructions="""
    You are an expert at inferring company pain points and challenges from their content.

    APPROACH:
    - Look at what problems they solve for THEIR customers
    - Infer: If they solve X for customers, they likely struggle with Y internally
    - Industry-common pain points for their market
    - Gaps or emphasis in their messaging
    - What they talk about vs. what they don't

    For each pain point:
    - Description: Clear statement of the pain/challenge
    - Category: operational, strategic, technical, market, or growth
    - Evidence: Specific evidence from their content that suggests this pain
    - Affected personas: Which job titles/roles likely feel this pain (e.g., "VP Sales", "CMO", "Head of RevOps")
    - Confidence:
      * high - Explicitly mentioned or very obvious
      * medium - Implied by their content or business model
      * low - Inferred from industry norms

    EXAMPLES OF INFERENCE:
    - If they emphasize "easy integration" → they likely had integration pain previously
    - If they're in regulated industry → compliance is likely a pain
    - If they show fast growth metrics → scaling challenges are likely
    - If they solve "personalization at scale" → they likely struggled with it
    - If they highlight "time savings" for customers → efficiency is their pain point

    MAPPING TO PERSONAS:
    For each pain, identify which roles feel it:
    - Sales process issues → VP Sales, Sales Ops, Revenue Ops
    - Marketing effectiveness → CMO, VP Marketing, Demand Gen
    - Tech/integration → CTO, Head of Engineering, IT
    - Strategic/growth → CEO, COO, Chief Revenue Officer
    - Operational efficiency → COO, Operations teams

    Extract 3-7 pain points total. Be specific and evidence-based.
    Focus on pain points that would make them receptive to sales outreach.
    """,
    output_schema=PainPointsResult
)
