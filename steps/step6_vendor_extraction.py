"""
Step 6: Vendor Element Extraction
Extracts 8 key GTM elements from vendor content using specialized AI agents.
Runs in parallel for efficiency: offerings, case studies, testimonials, clients,
differentiators, objections, buyer personas, and competitors.
"""

from agno.workflow.types import StepInput, StepOutput
from agents.vendor_specialists.offerings_extractor import offerings_extractor
from agents.vendor_specialists.case_study_extractor import case_study_extractor
from agents.vendor_specialists.proof_points_extractor import proof_points_extractor
from agents.vendor_specialists.value_prop_extractor import value_prop_extractor
from agents.vendor_specialists.customer_extractor import customer_extractor
from agents.vendor_specialists.use_case_extractor import use_case_extractor
from agents.vendor_specialists.persona_extractor import persona_extractor
from agents.vendor_specialists.differentiator_extractor import differentiator_extractor
from utils.workflow_helpers import create_error_response


def extract_offerings(step_input: StepInput) -> StepOutput:
    """Extract all product/service offerings"""
    try:
        # Get vendor content from Step 5
        scrape_data = step_input.get_step_content("batch_scrape")

        if not scrape_data:
            return create_error_response("No batch scrape data available")

        vendor_content = scrape_data.get("vendor_content", {})

        if not vendor_content:
            print("⚠️  No vendor content found - returning empty offerings")
            return StepOutput(content={"offerings": []}, success=True)

        # Combine all content with URL labels
        full_content = "\n\n---\n\n".join([
            f"URL: {url}\n\n{content}"
            for url, content in vendor_content.items()
        ])

        print(f"🔍 Extracting offerings from {len(vendor_content)} vendor pages...")

        # Run agent
        response = offerings_extractor.run(
            input=f"Extract all offerings from this content:\n\n{full_content}"
        )

        # Validate agent response
        if not response.content or not hasattr(response.content, 'offerings'):
            return create_error_response("Agent failed to extract offerings")

        offerings = response.content.offerings
        print(f"✅ Found {len(offerings)} offerings")

        return StepOutput(content={"offerings": [o.model_dump() for o in offerings]}, success=True)

    except Exception as e:
        return create_error_response(f"Offerings extraction failed: {str(e)}")


def extract_case_studies(step_input: StepInput) -> StepOutput:
    """Extract all case studies"""
    try:
        scrape_data = step_input.get_step_content("batch_scrape")

        if not scrape_data:
            return create_error_response("No batch scrape data available")

        vendor_content = scrape_data.get("vendor_content", {})

        if not vendor_content:
            print("⚠️  No vendor content found - returning empty case studies")
            return StepOutput(content={"case_studies": []}, success=True)

        full_content = "\n\n---\n\n".join([
            f"URL: {url}\n\n{content}"
            for url, content in vendor_content.items()
        ])

        print(f"📚 Extracting case studies from {len(vendor_content)} vendor pages...")

        response = case_study_extractor.run(
            input=f"Extract all case studies:\n\n{full_content}"
        )

        # Validate agent response
        if not response.content or not hasattr(response.content, 'case_studies'):
            return create_error_response("Agent failed to extract case studies")

        case_studies = response.content.case_studies
        print(f"✅ Found {len(case_studies)} case studies")

        return StepOutput(content={"case_studies": [cs.model_dump() for cs in case_studies]}, success=True)

    except Exception as e:
        return create_error_response(f"Case studies extraction failed: {str(e)}")


def extract_proof_points(step_input: StepInput) -> StepOutput:
    """Extract all proof points"""
    try:
        scrape_data = step_input.get_step_content("batch_scrape")

        if not scrape_data:
            return create_error_response("No batch scrape data available")

        vendor_content = scrape_data.get("vendor_content", {})

        if not vendor_content:
            print("⚠️  No vendor content found - returning empty proof points")
            return StepOutput(content={"proof_points": []}, success=True)

        full_content = "\n\n---\n\n".join([
            f"URL: {url}\n\n{content}"
            for url, content in vendor_content.items()
        ])

        print(f"🏆 Extracting proof points from {len(vendor_content)} vendor pages...")

        response = proof_points_extractor.run(
            input=f"Extract all proof points:\n\n{full_content}"
        )

        # Validate agent response
        if not response.content or not hasattr(response.content, 'proof_points'):
            return create_error_response("Agent failed to extract proof points")

        proof_points = response.content.proof_points
        print(f"✅ Found {len(proof_points)} proof points")

        return StepOutput(content={"proof_points": [pp.model_dump() for pp in proof_points]}, success=True)

    except Exception as e:
        return create_error_response(f"Proof points extraction failed: {str(e)}")


def extract_value_props(step_input: StepInput) -> StepOutput:
    """Extract all value propositions"""
    try:
        scrape_data = step_input.get_step_content("batch_scrape")

        if not scrape_data:
            return create_error_response("No batch scrape data available")

        vendor_content = scrape_data.get("vendor_content", {})

        if not vendor_content:
            print("⚠️  No vendor content found - returning empty value propositions")
            return StepOutput(content={"value_propositions": []}, success=True)

        full_content = "\n\n---\n\n".join([
            f"URL: {url}\n\n{content}"
            for url, content in vendor_content.items()
        ])

        print(f"💎 Extracting value propositions from {len(vendor_content)} vendor pages...")

        response = value_prop_extractor.run(
            input=f"Extract all value propositions:\n\n{full_content}"
        )

        # Validate agent response
        if not response.content or not hasattr(response.content, 'value_propositions'):
            return create_error_response("Agent failed to extract value propositions")

        value_props = response.content.value_propositions
        print(f"✅ Found {len(value_props)} value propositions")

        return StepOutput(content={"value_propositions": [vp.model_dump() for vp in value_props]}, success=True)

    except Exception as e:
        return create_error_response(f"Value propositions extraction failed: {str(e)}")


def extract_customers(step_input: StepInput) -> StepOutput:
    """Extract all reference customers"""
    try:
        scrape_data = step_input.get_step_content("batch_scrape")

        if not scrape_data:
            return create_error_response("No batch scrape data available")

        vendor_content = scrape_data.get("vendor_content", {})

        if not vendor_content:
            print("⚠️  No vendor content found - returning empty customers")
            return StepOutput(content={"reference_customers": []}, success=True)

        full_content = "\n\n---\n\n".join([
            f"URL: {url}\n\n{content}"
            for url, content in vendor_content.items()
        ])

        print(f"🏢 Extracting reference customers from {len(vendor_content)} vendor pages...")

        response = customer_extractor.run(
            input=f"Extract all reference customers:\n\n{full_content}"
        )

        # Validate agent response
        if not response.content or not hasattr(response.content, 'reference_customers'):
            return create_error_response("Agent failed to extract reference customers")

        customers = response.content.reference_customers
        print(f"✅ Found {len(customers)} reference customers")

        return StepOutput(content={"reference_customers": [c.model_dump() for c in customers]}, success=True)

    except Exception as e:
        return create_error_response(f"Reference customers extraction failed: {str(e)}")


def extract_use_cases(step_input: StepInput) -> StepOutput:
    """Extract all use cases"""
    try:
        scrape_data = step_input.get_step_content("batch_scrape")

        if not scrape_data:
            return create_error_response("No batch scrape data available")

        vendor_content = scrape_data.get("vendor_content", {})

        if not vendor_content:
            print("⚠️  No vendor content found - returning empty use cases")
            return StepOutput(content={"use_cases": []}, success=True)

        full_content = "\n\n---\n\n".join([
            f"URL: {url}\n\n{content}"
            for url, content in vendor_content.items()
        ])

        print(f"🎯 Extracting use cases from {len(vendor_content)} vendor pages...")

        response = use_case_extractor.run(
            input=f"Extract all use cases:\n\n{full_content}"
        )

        # Validate agent response
        if not response.content or not hasattr(response.content, 'use_cases'):
            return create_error_response("Agent failed to extract use cases")

        use_cases = response.content.use_cases
        print(f"✅ Found {len(use_cases)} use cases")

        return StepOutput(content={"use_cases": [uc.model_dump() for uc in use_cases]}, success=True)

    except Exception as e:
        return create_error_response(f"Use cases extraction failed: {str(e)}")


def extract_personas(step_input: StepInput) -> StepOutput:
    """
    Extract vendor's ICP (Ideal Customer Profile) personas

    These are the types of buyers the vendor typically sells to,
    NOT specific personas at the prospect company.
    """
    try:
        scrape_data = step_input.get_step_content("batch_scrape")

        if not scrape_data:
            return create_error_response("No batch scrape data available")

        vendor_content = scrape_data.get("vendor_content", {})

        if not vendor_content:
            print("⚠️  No vendor content found - returning empty ICP personas")
            return StepOutput(content={"vendor_icp_personas": []}, success=True)

        full_content = "\n\n---\n\n".join([
            f"URL: {url}\n\n{content}"
            for url, content in vendor_content.items()
        ])

        print(f"👥 Extracting vendor ICP personas from {len(vendor_content)} vendor pages...")

        response = persona_extractor.run(
            input=f"Extract vendor's ICP (Ideal Customer Profile) personas - the types of buyers they typically sell to:\n\n{full_content}"
        )

        # Validate agent response
        if not response.content or not hasattr(response.content, 'target_personas'):
            return create_error_response("Agent failed to extract personas")

        personas = response.content.target_personas
        print(f"✅ Found {len(personas)} vendor ICP personas")

        return StepOutput(content={"vendor_icp_personas": [p.model_dump() for p in personas]}, success=True)

    except Exception as e:
        return create_error_response(f"Vendor ICP personas extraction failed: {str(e)}")


def extract_differentiators(step_input: StepInput) -> StepOutput:
    """Extract all competitive differentiators"""
    try:
        scrape_data = step_input.get_step_content("batch_scrape")

        if not scrape_data:
            return create_error_response("No batch scrape data available")

        vendor_content = scrape_data.get("vendor_content", {})

        if not vendor_content:
            print("⚠️  No vendor content found - returning empty differentiators")
            return StepOutput(content={"differentiators": []}, success=True)

        full_content = "\n\n---\n\n".join([
            f"URL: {url}\n\n{content}"
            for url, content in vendor_content.items()
        ])

        print(f"⚡ Extracting differentiators from {len(vendor_content)} vendor pages...")

        response = differentiator_extractor.run(
            input=f"Extract all competitive differentiators:\n\n{full_content}"
        )

        # Validate agent response
        if not response.content or not hasattr(response.content, 'differentiators'):
            return create_error_response("Agent failed to extract differentiators")

        differentiators = response.content.differentiators
        print(f"✅ Found {len(differentiators)} differentiators")

        return StepOutput(content={"differentiators": [d.model_dump() for d in differentiators]}, success=True)

    except Exception as e:
        return create_error_response(f"Differentiators extraction failed: {str(e)}")
