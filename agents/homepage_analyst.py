"""
Homepage Analyst Agent
Analyzes homepage content to extract company basics, offerings, trust signals, and CTAs.
Uses OpenAI GPT-4o for complex reasoning and analysis.
"""

from agno.agent import Agent
import config

homepage_analyst = Agent(
    name="Homepage Analyst",
    model=config.DEFAULT_MODEL,
    description="B2B company analyst specializing in homepage analysis, extracting company basics, offerings, trust signals, and calls to action.",
    instructions=[
        "Analyze the homepage content and extract key company information.",
        "Extract COMPANY BASICS: company name, tagline/positioning statement, primary value proposition, and industry/market category.",
        "Extract OFFERINGS: main products or services mentioned, key features highlighted, and target audience indicators.",
        "Extract TRUST SIGNALS: customer logos visible, testimonials or quotes, statistics or metrics, and notable achievements.",
        "Extract CALL TO ACTION: primary CTA (demo, trial, contact, etc.) and target personas implied by CTAs.",
        "Return a structured analysis focusing on what this company does and who they serve.",
        "Keep it concise but comprehensive.",
    ],
    markdown=True
)
