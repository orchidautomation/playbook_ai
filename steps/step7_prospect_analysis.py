from agno.workflow.types import StepInput, StepOutput
from agents.prospect_specialists.company_analyst import company_analyst
from agents.prospect_specialists.pain_point_analyst import pain_point_analyst
from agents.prospect_specialists.buyer_persona_analyst import buyer_persona_analyst
from utils.workflow_helpers import get_parallel_step_content, create_error_response
import json


def analyze_company_profile(step_input: StepInput) -> StepOutput:
    """Extract minimal company profile from prospect content"""
    try:
        # Get prospect content from Step 5
        scrape_data = step_input.get_step_content("batch_scrape")

        if not scrape_data:
            return create_error_response("No batch scrape data available")

        prospect_content = scrape_data.get("prospect_content", {})

        if not prospect_content:
            return create_error_response("No prospect content available")

        # Combine prospect content
        full_content = "\n\n---\n\n".join([
            f"URL: {url}\n\n{content}"
            for url, content in prospect_content.items()
        ])

        print(f"🏢 Analyzing company profile from {len(prospect_content)} prospect pages...")

        # Run agent
        response = company_analyst.run(
            input=f"Extract company profile from this content:\n\n{full_content}"
        )

        # Validate agent response
        if not response or not response.content or not response.content.company_profile:
            return create_error_response("Agent failed to extract company profile")

        company_profile = response.content.company_profile
        print(f"✅ Company profile extracted: {company_profile.company_name}")

        return StepOutput(
            content={"company_profile": company_profile.model_dump()},
            success=True
        )

    except Exception as e:
        return create_error_response(f"Error analyzing company profile: {str(e)}")


def analyze_pain_points(step_input: StepInput) -> StepOutput:
    """Infer prospect pain points from their content"""
    try:
        # Get prospect content from Step 5
        scrape_data = step_input.get_step_content("batch_scrape")

        if not scrape_data:
            return create_error_response("No batch scrape data available")

        prospect_content = scrape_data.get("prospect_content", {})

        if not prospect_content:
            return create_error_response("No prospect content found - cannot analyze pain points")

        # Combine prospect content
        full_content = "\n\n---\n\n".join([
            f"URL: {url}\n\n{content}"
            for url, content in prospect_content.items()
        ])

        print(f"💡 Inferring pain points from {len(prospect_content)} prospect pages...")

        # Run agent
        response = pain_point_analyst.run(
            input=f"Infer pain points from this company's content:\n\n{full_content}"
        )

        # Validate agent response
        if not response or not response.content or not response.content.pain_points:
            return create_error_response("Agent failed to identify pain points")

        pain_points = response.content.pain_points
        print(f"✅ Identified {len(pain_points)} pain points")

        return StepOutput(
            content={"pain_points": [pp.model_dump() for pp in pain_points]},
            success=True
        )

    except Exception as e:
        return create_error_response(f"Error analyzing pain points: {str(e)}")


def identify_buyer_personas(step_input: StepInput) -> StepOutput:
    """
    Identify target buyer personas at the prospect company (ABM buying committee)

    IMPORTANT: This identifies specific personas AT THE PROSPECT COMPANY
    that the vendor should target for outreach. This is different from
    the vendor's typical ICP extracted in Step 6.

    This is the ABM "buying committee" - the specific people to call at
    this specific account.
    """
    try:
        # Get vendor elements from Step 6 (vendor_element_extraction Parallel block)
        vendor_offerings = get_parallel_step_content(step_input, "vendor_element_extraction", "extract_offerings")
        vendor_case_studies = get_parallel_step_content(step_input, "vendor_element_extraction", "extract_case_studies")
        vendor_value_props = get_parallel_step_content(step_input, "vendor_element_extraction", "extract_value_props")
        vendor_use_cases = get_parallel_step_content(step_input, "vendor_element_extraction", "extract_use_cases")
        vendor_personas = get_parallel_step_content(step_input, "vendor_element_extraction", "extract_personas")
        vendor_differentiators = get_parallel_step_content(step_input, "vendor_element_extraction", "extract_differentiators")

        # Get prospect intelligence from Step 7a (prospect_context_analysis Parallel block)
        company_data = get_parallel_step_content(step_input, "prospect_context_analysis", "analyze_company")
        pain_points_data = get_parallel_step_content(step_input, "prospect_context_analysis", "analyze_pain_points")

        if not company_data or not vendor_value_props:
            return create_error_response("Missing vendor or prospect data for persona identification")

        # Build comprehensive intelligence package
        vendor_intelligence = {
            "offerings": vendor_offerings.get("offerings", []) if vendor_offerings else [],
            "case_studies": vendor_case_studies.get("case_studies", []) if vendor_case_studies else [],
            "value_propositions": vendor_value_props.get("value_propositions", []) if vendor_value_props else [],
            "use_cases": vendor_use_cases.get("use_cases", []) if vendor_use_cases else [],
            "vendor_icp_personas": vendor_personas.get("vendor_icp_personas", []) if vendor_personas else [],
            "differentiators": vendor_differentiators.get("differentiators", []) if vendor_differentiators else []
        }

        prospect_intelligence = {
            "company_profile": company_data.get("company_profile", {}) if company_data else {},
            "pain_points": pain_points_data.get("pain_points", []) if pain_points_data else []
        }

        print(f"🎯 Identifying target buyer personas using vendor + prospect intelligence...")
        print(f"   Vendor elements: {sum(len(v) if isinstance(v, list) else 1 for v in vendor_intelligence.values())} items")
        print(f"   Prospect context: {len(prospect_intelligence['pain_points'])} pain points identified")

        # Build comprehensive prompt
        prompt = f"""
ABM CONTEXT:
This is an Account-Based Marketing motion. You are identifying the buying committee at a SPECIFIC prospect company.
- VENDOR = the company selling (trying to win this account)
- PROSPECT = the target account (the company vendor wants as a customer)

VENDOR INTELLIGENCE (what the vendor offers):
{json.dumps(vendor_intelligence, indent=2)}

PROSPECT INTELLIGENCE (the target account):
{json.dumps(prospect_intelligence, indent=2)}

YOUR TASK:
Identify the 3-5 KEY BUYER PERSONAS at the PROSPECT company that the VENDOR should target for sales outreach.

These are specific roles at THIS prospect company, not generic personas.
Example: If prospect is "Acme Corp", you're identifying "VP of Sales at Acme Corp who would buy from vendor".

For each persona:
- Specific job title (at the prospect company)
- Why they'd care about vendor's solution
- Their pain points (based on prospect's business)
- Their goals
- Suggested talking points (connect vendor's value props to their needs)
- Priority score (1-10)

Return 3-5 personas ranked by priority (highest first).
Make this actionable - these are the specific people at this account that sales reps will call.
"""

        # Run agent
        response = buyer_persona_analyst.run(input=prompt)

        # Validate agent response
        if not response or not response.content or not response.content.target_buyer_personas:
            return create_error_response("Agent failed to identify buyer personas")

        personas = response.content.target_buyer_personas
        print(f"✅ Identified {len(personas)} target buyer personas")

        # Print summary
        for i, persona in enumerate(personas, 1):
            print(f"   {i}. {persona.persona_title} (Priority: {persona.priority_score}/10)")

        return StepOutput(
            content={"target_buyer_personas": [p.model_dump() for p in personas]},
            success=True
        )

    except Exception as e:
        return create_error_response(f"Error identifying buyer personas: {str(e)}")
