"""
Step 4: URL Prioritization
Selects the most valuable URLs to scrape from both vendor and prospect websites.
Sequential step (runs after parallel homepage analysis).
"""

from agno.workflow.types import StepInput, StepOutput
from agents.url_prioritizer import url_prioritizer
from utils.workflow_helpers import get_parallel_step_content, create_error_response, create_success_response
from config import MAX_URLS_FOR_PRIORITIZATION


def prioritize_urls(step_input: StepInput) -> StepOutput:
    """
    Prioritize URLs from both companies using AI.

    Args:
        step_input: StepInput with access to Step 1 outputs (validate_vendor, validate_prospect)

    Returns:
        StepOutput with selected URLs for both companies
    """
    # Get URLs from Step 1 using helper function
    vendor_data = get_parallel_step_content(step_input, "parallel_validation", "validate_vendor")
    prospect_data = get_parallel_step_content(step_input, "parallel_validation", "validate_prospect")

    if not vendor_data or not isinstance(vendor_data, dict):
        return create_error_response("Vendor validation failed: no data")

    if "error" in vendor_data:
        return create_error_response(f"Vendor validation failed: {vendor_data['error']}")

    if not prospect_data or not isinstance(prospect_data, dict):
        return create_error_response("Prospect validation failed: no data")

    if "error" in prospect_data:
        return create_error_response(f"Prospect validation failed: {prospect_data['error']}")

    vendor_urls = vendor_data.get("vendor_urls", [])
    prospect_urls = prospect_data.get("prospect_urls", [])

    if not vendor_urls or not prospect_urls:
        return create_error_response("No URLs found from Step 1 validation")

    print(f"🎯 Prioritizing {len(vendor_urls)} vendor URLs and {len(prospect_urls)} prospect URLs...")

    # Prepare input for agent - limit URLs to avoid token overflow
    prompt = f"""
VENDOR URLs ({len(vendor_urls)} total):
{chr(10).join(vendor_urls[:MAX_URLS_FOR_PRIORITIZATION])}

PROSPECT URLs ({len(prospect_urls)} total):
{chr(10).join(prospect_urls[:MAX_URLS_FOR_PRIORITIZATION])}

Select the top 10-15 most valuable URLs from each company for sales intelligence gathering.
"""

    try:
        # Run agent
        response = url_prioritizer.run(input=prompt)
        result = response.content

        # Validate response structure
        if not hasattr(result, 'vendor_selected_urls') or not hasattr(result, 'prospect_selected_urls'):
            return create_error_response("Agent returned unexpected response structure")

        if not result.vendor_selected_urls or not result.prospect_selected_urls:
            return create_error_response("Agent returned empty URL lists")

        # Extract URLs from structured output
        vendor_selected = [item.url for item in result.vendor_selected_urls]
        prospect_selected = [item.url for item in result.prospect_selected_urls]

        print(f"✅ Selected {len(vendor_selected)} vendor URLs and {len(prospect_selected)} prospect URLs")

        # Serialize Pydantic models to dicts for workflow compatibility
        return create_success_response({
            "vendor_selected_urls": vendor_selected,
            "prospect_selected_urls": prospect_selected,
            "vendor_url_details": [item.model_dump() for item in result.vendor_selected_urls],
            "prospect_url_details": [item.model_dump() for item in result.prospect_selected_urls]
        })

    except Exception as e:
        return create_error_response(f"URL prioritization failed ({type(e).__name__}): {str(e)}")
