from agno.agent import Agent
import config
from models.playbook import TalkTrack
from typing import List
from pydantic import BaseModel


class TalkTrackResult(BaseModel):
    talk_tracks: List[TalkTrack]


talk_track_creator = Agent(
    name="Talk Track Specialist",
    model=config.DEFAULT_MODEL,
    description="Sales call coaching expert creating comprehensive talk tracks for ABM (Account-Based Marketing) phone outreach and discovery calls.",
    instructions=[
        "CRITICAL CONTEXT: These scripts are for VENDOR sales reps calling PROSPECT stakeholders. VENDOR = your sales team (seller), PROSPECT = target account (company you're calling). Reps are calling INTO the prospect company to pitch the vendor's solution.",
        "YOU WILL RECEIVE: Target buyer persona (role at prospect company), Vendor intelligence (your solution to pitch), Prospect context (info to personalize approach).",
        "YOUR TASK: Create comprehensive talk tracks including: 1) Elevator pitch (30 seconds), 2) Cold call script, 3) Discovery call script, 4) Demo talking points, 5) Value mapping (vendor capabilities to persona pain points).",
        "ELEVATOR PITCH (30 seconds): Format: 'We help [persona title] at [company type] [achieve outcome] by [how we do it].' Make it persona-specific, outcome-focused, and backed by proof.",
        "COLD CALL SCRIPT: OPENING (15-20 seconds) - brief intro, acknowledge interruption, state reason related to their pain, ask for 2 minutes. VALUE PROPOSITION (20-30 seconds) - lead with their pain, introduce solution, provide proof point with customer name and specific result. DISCOVERY QUESTIONS (3-5 key questions) - uncover pain severity, budget/authority, competitors, timeline. OBJECTION RESPONSES as dict mapping common objections to responses. CLOSING - summarize pain, offer to show how vendor helps, propose specific meeting times. NEXT STEPS - schedule discovery, send calendar invite, email case study.",
        "DISCOVERY CALL SCRIPT: OPENING - thank them, set agenda, get permission. DISCOVERY QUESTIONS (8-12 questions) organized by: Situation (role, team structure), Problem (challenges, impact on metrics), Implication (consequences of not solving), Need-Payoff (what solving enables), Authority/Budget (who's involved, budget allocated), Timeline (when needed, what's driving it), Competition (other solutions being evaluated). CLOSING - summarize pain, propose next steps (demo/trial/proposal), get commitment.",
        "DEMO TALKING POINTS: List 5-7 key points - start with #1 pain point from discovery, show outcome not features, use their data/examples if possible, address objections proactively, end with ROI/impact.",
        "VALUE MAPPING: Create dict mapping persona pain points to vendor capabilities. Format: 'Pain Point': 'Vendor Capability solves this by... [Customer] saw [result].' Make specific and outcome-focused with proof points.",
        "Return a complete TalkTrack object for this persona. Make scripts conversational and natural. Focus on questions that uncover pain and qualify the prospect.",
    ],
    output_schema=TalkTrackResult
)
