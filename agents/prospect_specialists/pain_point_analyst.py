from agno.agent import Agent
import config
from models.prospect_intelligence import PainPoint
from typing import List
from pydantic import BaseModel


class PainPointsResult(BaseModel):
    pain_points: List[PainPoint]


pain_point_analyst = Agent(
    name="Pain Point Analyst",
    model=config.REASONING_MODEL,
    description="Expert at inferring company pain points and challenges from website content and business context for sales intelligence.",
    instructions=[
        "APPROACH: Look at what problems they solve for THEIR customers, then infer internal struggles. Consider industry-common pain points, gaps in messaging, and what they emphasize vs. don't mention.",
        "For each pain point, capture: Description (clear statement of pain/challenge), Category (operational/strategic/technical/market/growth), Evidence (specific content suggesting this pain), Affected personas (job titles feeling this pain), and Confidence (high=explicit, medium=implied, low=industry inference).",
        "INFERENCE EXAMPLES: 'Easy integration' emphasis suggests integration pain; regulated industry suggests compliance pain; fast growth metrics suggest scaling challenges; 'personalization at scale' suggests they struggled with it; 'time savings' emphasis suggests efficiency is their pain point.",
        "MAP TO PERSONAS: Sales process issues affect VP Sales/Sales Ops/Revenue Ops; Marketing effectiveness affects CMO/VP Marketing/Demand Gen; Tech/integration affects CTO/Head of Engineering/IT; Strategic/growth affects CEO/COO/Chief Revenue Officer; Operational efficiency affects COO/Operations teams.",
        "Extract 3-7 pain points total. Be specific and evidence-based.",
        "Focus on pain points that would make them receptive to sales outreach.",
    ],
    output_schema=PainPointsResult
)
