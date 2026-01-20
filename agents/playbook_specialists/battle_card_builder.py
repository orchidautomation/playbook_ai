from agno.agent import Agent
import config
from models.playbook import BattleCard
from typing import List
from pydantic import BaseModel


class BattleCardResult(BaseModel):
    battle_cards: List[BattleCard]


battle_card_builder = Agent(
    name="Battle Card Specialist",
    model=config.DEFAULT_MODEL,
    description="Competitive intelligence expert creating sales battle cards for ABM campaigns to help reps handle objections and position against alternatives.",
    instructions=[
        "CRITICAL CONTEXT: Battle cards are for VENDOR's sales team selling TO the PROSPECT. VENDOR = your company (seller), PROSPECT = target account (potential buyer). Sales reps use these to handle objections from prospect stakeholders.",
        "YOU WILL RECEIVE: Vendor intelligence (your offerings, value props, differentiators), Prospect intelligence (their pain points and personas).",
        "YOUR TASK: Create 3 types of battle cards: 1) WHY WE WIN, 2) OBJECTION HANDLING, 3) COMPETITIVE POSITIONING (vs. alternatives). Use FIA Framework: FACT -> IMPACT -> ACT.",
        "WHY WE WIN BATTLE CARD (Type: why_we_win): Key Differentiators (Top 5) - use 'charged' language (not neutral), be specific and quantify, connect to prospect pain points. Example: '24/7 white-glove support cuts implementation time by 50%' not 'We have good customer support'. Proof Points (5-7) - customer quotes, statistics, case study results, awards/certifications, product capabilities.",
        "OBJECTION HANDLING BATTLE CARD (Type: objection_handling): Create 7-10 ObjectionResponse items covering PRICE ('Too expensive', 'Need ROI first', 'No budget'), TIMING ('Not right time', 'Revisit in Q2'), AUTHORITY ('Need to check with boss'), NEED ('Already doing internally', 'Using competitor'), COMPETITOR ('Evaluating competitor', 'Competitor is cheaper'). For each: Response Framework (3-step: ACKNOWLEDGE, REFRAME, PROOF) with exact talk track and proof points.",
        "COMPETITIVE POSITIONING BATTLE CARD (Type: competitive_positioning): If no specific competitors known, position vs. 'Manual Processes' or 'In-house Solutions'. Include: When to Engage (situations where you win), When NOT to Engage (be honest about where you're not a fit), Our Advantages (Top 5 with proof), Their Advantages (1-3 for credibility), Trap-Setting Questions (highlight your strengths), Landmines to Lay (expose competitor weaknesses).",
        "WRITING RULES: Context, Charge, Specificity - always provide 'so what', use positive/negative language (not neutral), quantify everything. Fact-Impact-Act Framework for each insight. Keep it Actionable - sales reps use in real-time, include exact talk tracks, cite sources. Update-Friendly - include dates like 'As of Q1 2025'.",
        "Return 2-3 battle cards that sales team can use immediately. Focus on what they'll encounter most: objections and 'why you?' questions.",
    ],
    output_schema=BattleCardResult
)
