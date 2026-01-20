from agno.agent import Agent
import config
from models.prospect_intelligence import TargetBuyerPersona
from typing import List
from pydantic import BaseModel


class BuyerPersonasResult(BaseModel):
    target_buyer_personas: List[TargetBuyerPersona]


buyer_persona_analyst = Agent(
    name="Strategic Buyer Persona Analyst",
    model=config.REASONING_MODEL,
    description="Strategic sales intelligence analyst identifying key buyer personas at prospect companies that vendors should target for outreach.",
    instructions=[
        "YOU WILL RECEIVE: 1) VENDOR INTELLIGENCE (offerings, value props, use cases, personas they target) and 2) PROSPECT INTELLIGENCE (what the prospect does, their pain points, company profile).",
        "YOUR TASK: Identify 3-5 KEY BUYER PERSONAS at the prospect that the vendor should reach out to.",
        "For each persona provide: persona_title (specific job title like 'VP of Sales', 'CMO', 'Head of Revenue Operations'), department (function like Sales, Marketing, Revenue Ops, Product, Engineering).",
        "Provide why_they_care: 2-3 sentences explaining WHY this persona would care about the vendor's solution. Connect vendor's value prop to their responsibilities and be specific about business impact.",
        "Provide pain_points: 3-5 specific pain points this role faces (tied to prospect's business and industry). Example: ['Scaling personalized outreach across growing team', 'Inconsistent messaging quality across reps', 'Low email response rates'].",
        "Provide goals: 3-5 goals this persona is trying to achieve (what success looks like). Example: ['Increase pipeline velocity', 'Improve win rates', 'Scale sales productivity'].",
        "Provide suggested_talking_points: 3-5 specific talking points for sales outreach. Connect vendor solution to their pain/goals using vendor's actual value props and differentiators.",
        "Provide priority_score: 1-10 (10 = highest priority). Base on: solution fit, seniority, decision-making power, budget ownership. Typically: C-level = 8-10, VP-level = 7-9, Director/Head = 5-7, Manager = 3-5.",
        "PRIORITIZATION LOGIC: Who has budget/decision authority? Who feels the pain most directly? Who owns the metrics vendor improves? Who is vendor's typical buyer persona?",
        "COMMON B2B PERSONAS: Sales tools target VP Sales/CRO/Head of Sales Ops; Marketing tools target CMO/VP Marketing/Head of Demand Gen; RevOps tools target CRO/VP Revenue Ops; Product tools target VP Product/Product Managers; Data/Analytics target VP Analytics/CDO/Head of BI.",
        "Return 3-5 personas ranked by priority_score (highest first). Be strategic - these are the people sales reps will actually call. Make talking points specific to vendor's actual offerings.",
    ],
    output_schema=BuyerPersonasResult
)
