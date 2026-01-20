"""
Playbook Models - Phase 4
Production-ready sales playbook data structures
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal
from models.common import Source


# ============================================================================
# EMAIL SEQUENCE MODELS (Sequencer-Ready)
# ============================================================================

class EmailTouch(BaseModel):
    """
    Single email touchpoint - designed for direct import to email sequencers
    (Lemlist, Smartlead, Instantly, etc.)
    """
    touch_number: int = Field(ge=1, le=4, description="Touch number in sequence (1-4)")
    day: int = Field(ge=1, description="Day number in sequence (1, 3, 7, 14)")
    subject: str = Field(description="Email subject line - maps to sequencer 'subject' field")
    body: str = Field(description="Email body with personalization tokens - maps to sequencer 'body' field")
    personalization_notes: List[str] = Field(
        default_factory=list,
        description="Implementation notes for personalizing this email"
    )
    call_to_action: str = Field(description="What you're asking the recipient to do")


class EmailSequence(BaseModel):
    """4-touch email sequence for a specific buyer persona"""
    persona_title: str = Field(description="Target persona (e.g., 'CMO', 'VP Sales')")
    sequence_name: str = Field(description="Name of sequence (e.g., 'CMO - 4 Touch Sequence')")
    total_days: int = Field(default=14, description="Total length in days")
    total_touches: int = Field(default=4, description="Total email touches")
    objective: str = Field(description="Goal of sequence (e.g., 'Book discovery call')")
    touches: List[EmailTouch] = Field(description="All 4 email touches in order")
    best_practices: List[str] = Field(
        default_factory=list,
        description="Tips for executing this sequence effectively"
    )


# ============================================================================
# TALK TRACK MODELS
# ============================================================================

class DiscoveryQuestion(BaseModel):
    """Question to ask during discovery call"""
    question: str = Field(description="The question to ask")
    purpose: str = Field(description="Why ask this / what you're uncovering")
    follow_up_questions: List[str] = Field(
        default_factory=list,
        description="Follow-up questions based on their answer"
    )


class CallScript(BaseModel):
    """Script for a specific type of sales call"""
    script_type: Literal["cold_call", "discovery", "demo", "follow_up"] = Field(
        description="Type of call script"
    )
    persona_title: str = Field(description="Who you're calling")
    opening: str = Field(description="How to open the call (first 30 seconds)")
    value_proposition: str = Field(description="Core value prop for this persona")
    discovery_questions: List[DiscoveryQuestion] = Field(
        default_factory=list,
        description="Questions to ask during call"
    )
    objection_responses: Dict[str, str] = Field(
        default_factory=dict,
        description="Common objections and responses"
    )
    closing: str = Field(description="How to close the call")
    next_steps: List[str] = Field(
        default_factory=list,
        description="Typical next steps to propose"
    )


class TalkTrack(BaseModel):
    """Complete talk track for a buyer persona"""
    persona_title: str = Field(description="Target persona")
    elevator_pitch: str = Field(description="30-second pitch for this persona")
    cold_call_script: CallScript
    discovery_script: CallScript
    demo_talking_points: List[str] = Field(
        default_factory=list,
        description="Key points to cover in demo"
    )
    value_mapping: Dict[str, str] = Field(
        default_factory=dict,
        description="Map vendor capabilities to persona's pain points"
    )


# ============================================================================
# BATTLE CARD MODELS
# ============================================================================

class ObjectionResponse(BaseModel):
    """How to handle a specific objection"""
    objection: str = Field(description="The objection")
    category: Literal["price", "timing", "authority", "need", "competitor"] = Field(
        description="Objection category"
    )
    response_framework: str = Field(
        description="How to respond (e.g., 'Acknowledge → Reframe → Proof')"
    )
    talk_track: str = Field(description="Exact words to say")
    proof_points: List[str] = Field(
        default_factory=list,
        description="Evidence to support your response"
    )


class CompetitivePositioning(BaseModel):
    """How to position against competitors or alternatives"""
    competitor_name: Optional[str] = Field(
        default=None,
        description="Competitor name or 'Manual Process' / 'In-house Solution'"
    )
    when_to_engage: List[str] = Field(
        default_factory=list,
        description="Situations where you should compete"
    )
    when_not_to_engage: List[str] = Field(
        default_factory=list,
        description="Situations where you shouldn't compete"
    )
    our_advantages: List[str] = Field(
        default_factory=list,
        description="Where we win"
    )
    their_advantages: List[str] = Field(
        default_factory=list,
        description="Where they win (be honest)"
    )
    trap_setting_questions: List[str] = Field(
        default_factory=list,
        description="Questions that highlight our strengths"
    )
    landmines_to_lay: List[str] = Field(
        default_factory=list,
        description="Points to raise that expose competitor weaknesses"
    )


class BattleCard(BaseModel):
    """Battle card for sales enablement"""
    title: str = Field(description="Battle card name")
    card_type: Literal["why_we_win", "objection_handling", "competitive_positioning"] = Field(
        description="Type of battle card"
    )
    persona_focus: Optional[str] = Field(
        default=None,
        description="Persona this card is tailored for (optional)"
    )
    key_differentiators: List[str] = Field(
        default_factory=list,
        description="Top differentiators to emphasize"
    )
    proof_points: List[str] = Field(
        default_factory=list,
        description="Stats, quotes, case studies to reference"
    )
    objection_responses: List[ObjectionResponse] = Field(
        default_factory=list,
        description="Objection handling responses"
    )
    competitive_positioning: List[CompetitivePositioning] = Field(
        default_factory=list,
        description="Competitive positioning guidance"
    )


# ============================================================================
# COMPLETE PLAYBOOK MODEL
# ============================================================================

class SalesPlaybook(BaseModel):
    """Complete sales playbook for vendor → prospect engagement"""

    # Metadata
    vendor_name: str = Field(description="Name of the vendor/seller company")
    prospect_name: str = Field(description="Name of the prospect/target company")
    generated_date: str = Field(description="Date the playbook was generated (ISO format)")

    # Executive Summary
    executive_summary: str = Field(
        description="2-3 paragraph summary: who to target, why they care, how to engage"
    )

    # Priority Personas
    priority_personas: List[str] = Field(
        description="Ordered list of persona titles by priority"
    )

    # Quick Wins
    quick_wins: List[str] = Field(
        default_factory=list,
        description="Top 5 immediate actions for sales team"
    )

    # Success Metrics
    success_metrics: Dict[str, str] = Field(
        default_factory=dict,
        description="KPIs to track (email open rate, response rate, etc.)"
    )

    # Email Sequences (1 per top persona)
    email_sequences: List[EmailSequence] = Field(
        default_factory=list,
        description="4-touch email sequences for each priority persona"
    )

    # Talk Tracks (1 per top persona)
    talk_tracks: List[TalkTrack] = Field(
        default_factory=list,
        description="Call scripts and talking points for each persona"
    )

    # Battle Cards
    battle_cards: List[BattleCard] = Field(
        default_factory=list,
        description="Competitive positioning and objection handling"
    )
