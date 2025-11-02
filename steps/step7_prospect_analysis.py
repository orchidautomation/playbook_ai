from agno.workflow.types import StepInput, StepOutput
from agents.prospect_specialists.company_analyst import company_analyst
from agents.prospect_specialists.pain_point_analyst import pain_point_analyst
from agents.prospect_specialists.buyer_persona_analyst import buyer_persona_analyst
import json


def analyze_company_profile(step_input: StepInput) -> StepOutput:
    """Extract minimal company profile from prospect content"""
    try:
        # Get prospect content from Step 5
        scrape_data = step_input.get_step_content("batch_scrape")

        if not scrape_data:
            return StepOutput(
                content={"error": "No batch scrape data available"},
                success=False
            )

        prospect_content = scrape_data.get("prospect_content", {})

        if not prospect_content:
            print("⚠️  No prospect content found")
            return StepOutput(
                content={"error": "No prospect content available"},
                success=False
            )

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

        company_profile = response.content.company_profile
        print(f"✅ Company profile extracted: {company_profile.company_name}")

        return StepOutput(
            content={"company_profile": company_profile.model_dump()},
            success=True
        )

    except Exception as e:
        print(f"❌ Error analyzing company profile: {str(e)}")
        return StepOutput(
            content={"error": str(e)},
            success=False
        )


def analyze_pain_points(step_input: StepInput) -> StepOutput:
    """Infer prospect pain points from their content"""
    try:
        # Get prospect content from Step 5
        scrape_data = step_input.get_step_content("batch_scrape")

        if not scrape_data:
            return StepOutput(
                content={"error": "No batch scrape data available", "pain_points": []},
                success=False
            )

        prospect_content = scrape_data.get("prospect_content", {})

        if not prospect_content:
            print("⚠️  No prospect content found")
            return StepOutput(content={"pain_points": []}, success=True)

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

        pain_points = response.content.pain_points
        print(f"✅ Identified {len(pain_points)} pain points")

        return StepOutput(
            content={"pain_points": [pp.model_dump() for pp in pain_points]},
            success=True
        )

    except Exception as e:
        print(f"❌ Error analyzing pain points: {str(e)}")
        return StepOutput(
            content={"error": str(e), "pain_points": []},
            success=False
        )


def identify_buyer_personas(step_input: StepInput) -> StepOutput:
    """Identify target buyer personas using vendor + prospect intelligence"""
    try:
        import ast

        # Helper function to deserialize Agno parallel outputs (stored as str(dict))
        def deserialize_step_data(data):
            """Agno stores parallel block outputs as str(dict), need to deserialize"""
            if isinstance(data, str):
                try:
                    return ast.literal_eval(data)
                except (ValueError, SyntaxError):
                    return None
            return data if isinstance(data, dict) else None

        # Get vendor elements from Step 6 (vendor_element_extraction Parallel block)
        vendor_extraction_results = step_input.get_step_content("vendor_element_extraction")
        vendor_extraction_results = deserialize_step_data(vendor_extraction_results)

        if not vendor_extraction_results:
            return StepOutput(
                content={"error": "No vendor extraction results available", "target_buyer_personas": []},
                success=False
            )

        vendor_offerings = deserialize_step_data(vendor_extraction_results.get("extract_offerings"))
        vendor_case_studies = deserialize_step_data(vendor_extraction_results.get("extract_case_studies"))
        vendor_value_props = deserialize_step_data(vendor_extraction_results.get("extract_value_props"))
        vendor_use_cases = deserialize_step_data(vendor_extraction_results.get("extract_use_cases"))
        vendor_personas = deserialize_step_data(vendor_extraction_results.get("extract_personas"))
        vendor_differentiators = deserialize_step_data(vendor_extraction_results.get("extract_differentiators"))

        # Get prospect intelligence from Step 7a (prospect_context_analysis Parallel block)
        prospect_context_results = step_input.get_step_content("prospect_context_analysis")
        prospect_context_results = deserialize_step_data(prospect_context_results)

        if not prospect_context_results:
            return StepOutput(
                content={"error": "No prospect context results available", "target_buyer_personas": []},
                success=False
            )

        company_data = deserialize_step_data(prospect_context_results.get("analyze_company"))
        pain_points_data = deserialize_step_data(prospect_context_results.get("analyze_pain_points"))

        if not company_data or not vendor_value_props:
            print("⚠️  Missing required data for persona identification")
            print(f"      company_data is None: {company_data is None}")
            print(f"      vendor_value_props is None: {vendor_value_props is None}")
            return StepOutput(
                content={"error": "Missing vendor or prospect data", "target_buyer_personas": []},
                success=False
            )

        # Build comprehensive intelligence package
        # The data from parallel blocks IS the actual content dict (not wrapped)
        # So vendor_offerings IS {"offerings": [...], "success": True}
        vendor_intelligence = {
            "offerings": vendor_offerings.get("offerings", []) if isinstance(vendor_offerings, dict) else [],
            "case_studies": vendor_case_studies.get("case_studies", []) if isinstance(vendor_case_studies, dict) else [],
            "value_propositions": vendor_value_props.get("value_propositions", []) if isinstance(vendor_value_props, dict) else [],
            "use_cases": vendor_use_cases.get("use_cases", []) if isinstance(vendor_use_cases, dict) else [],
            "target_personas": vendor_personas.get("target_personas", []) if isinstance(vendor_personas, dict) else [],
            "differentiators": vendor_differentiators.get("differentiators", []) if isinstance(vendor_differentiators, dict) else []
        }

        prospect_intelligence = {
            "company_profile": company_data.get("company_profile", {}) if isinstance(company_data, dict) else {},
            "pain_points": pain_points_data.get("pain_points", []) if isinstance(pain_points_data, dict) else []
        }

        print(f"🎯 Identifying target buyer personas using vendor + prospect intelligence...")
        print(f"   Vendor elements: {sum(len(v) if isinstance(v, list) else 1 for v in vendor_intelligence.values())} items")
        print(f"   Prospect context: {len(prospect_intelligence['pain_points'])} pain points identified")

        # Build comprehensive prompt
        prompt = f"""
VENDOR INTELLIGENCE:
{json.dumps(vendor_intelligence, indent=2)}

PROSPECT INTELLIGENCE:
{json.dumps(prospect_intelligence, indent=2)}

TASK:
Based on what the vendor offers and what the prospect company does/needs, identify the 3-5 KEY BUYER PERSONAS at the prospect company that the vendor should target for sales outreach.

For each persona:
- Specific job title
- Why they'd care about vendor's solution
- Their pain points (based on prospect's business)
- Their goals
- Suggested talking points (connect vendor's value props to their needs)
- Priority score (1-10)

Return 3-5 personas ranked by priority (highest first).
Make this actionable - these are the people sales reps will call.
"""

        # Run agent
        response = buyer_persona_analyst.run(input=prompt)

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
        print(f"❌ Error identifying buyer personas: {str(e)}")
        return StepOutput(
            content={"error": str(e), "target_buyer_personas": []},
            success=False
        )
