"""
Step 1: Domain Validation
Validates vendor and prospect domains and maps all discoverable URLs.
Runs in parallel for both domains.
"""

from agno.workflow.types import StepInput, StepOutput
from utils.firecrawl_helpers import map_website
from utils.workflow_helpers import validate_single_domain, create_error_response, create_success_response


def validate_vendor_domain(step_input: StepInput) -> StepOutput:
    """
    Validate vendor domain and map all URLs.

    Args:
        step_input: StepInput containing vendor_domain in input

    Returns:
        StepOutput with vendor_domain, vendor_urls, vendor_total_urls
    """
    try:
        # Defensive check
        if not step_input.input:
            return create_error_response("No workflow input provided")

        vendor_domain = getattr(step_input.input, 'vendor_domain', None)
        if not vendor_domain:
            return create_error_response("vendor_domain not provided in workflow input")

        # Validate domain format
        is_valid, error_msg = validate_single_domain(vendor_domain, "vendor_domain")
        if not is_valid:
            return create_error_response(error_msg)

        # Map the website
        print(f"🔍 Mapping vendor domain: {vendor_domain}")
        result = map_website(vendor_domain)  # Uses config.MAX_URLS_TO_MAP (5000)

        if not result["success"]:
            error_msg = f"Failed to map vendor domain: {result.get('error', 'Unknown error')}"
            return create_error_response(error_msg)

        print(f"✅ Found {result['total_urls']} URLs for vendor")

        return create_success_response({
            "vendor_domain": vendor_domain,
            "vendor_urls": result["urls"],
            "vendor_total_urls": result["total_urls"]
        })

    except Exception as e:
        return create_error_response(f"Vendor domain validation failed: {str(e)}")


def validate_prospect_domain(step_input: StepInput) -> StepOutput:
    """
    Validate prospect domain and map all URLs.

    Args:
        step_input: StepInput containing prospect_domain in input

    Returns:
        StepOutput with prospect_domain, prospect_urls, prospect_total_urls
    """
    try:
        # Defensive check
        if not step_input.input:
            return create_error_response("No workflow input provided")

        prospect_domain = getattr(step_input.input, 'prospect_domain', None)
        if not prospect_domain:
            return create_error_response("prospect_domain not provided in workflow input")

        # Validate domain format
        is_valid, error_msg = validate_single_domain(prospect_domain, "prospect_domain")
        if not is_valid:
            return create_error_response(error_msg)

        # Map the website
        print(f"🔍 Mapping prospect domain: {prospect_domain}")
        result = map_website(prospect_domain)  # Uses config.MAX_URLS_TO_MAP (5000)

        if not result["success"]:
            error_msg = f"Failed to map prospect domain: {result.get('error', 'Unknown error')}"
            return create_error_response(error_msg)

        print(f"✅ Found {result['total_urls']} URLs for prospect")

        return create_success_response({
            "prospect_domain": prospect_domain,
            "prospect_urls": result["urls"],
            "prospect_total_urls": result["total_urls"]
        })

    except Exception as e:
        return create_error_response(f"Prospect domain validation failed: {str(e)}")
