from agno.agent import Agent
import config
from models.vendor_elements import ValueProposition
from typing import List
from pydantic import BaseModel


class ValuePropositionsExtractionResult(BaseModel):
    value_propositions: List[ValueProposition]


value_prop_extractor = Agent(
    name="Value Proposition Extractor",
    model=config.EXTRACTION_MODEL,  # gpt-4o-mini for fast extraction
    description="Expert at identifying core value propositions, positioning statements, and outcome-based benefits from B2B company content.",
    instructions=[
        "Extract value propositions - the core benefits and outcomes promised to customers.",
        "For each value prop, capture: Statement (concise, compelling), Benefits (specific benefits delivered), Differentiation (what makes it unique), Target persona (who it appeals to), and Sources (URLs with page_type).",
        "Look for homepage hero sections, about page positioning, product benefit statements, 'Why choose us' sections, main taglines and headlines, and customer outcome promises.",
        "Focus on outcome-based value, not just feature lists. Look for statements about what customers achieve or gain.",
        "Examples of value props: 'Close deals 3x faster', 'Transform customer engagement', 'Simplify complex workflows', 'Drive revenue growth'.",
        "Extract both primary value prop and secondary/supporting value propositions.",
    ],
    output_schema=ValuePropositionsExtractionResult
)
