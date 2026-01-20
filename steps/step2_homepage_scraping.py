"""
Step 2: Homepage Scraping
Scrapes vendor and prospect homepages.
Runs in parallel for both homepages.
"""

from agno.workflow.types import StepInput, StepOutput
from utils.firecrawl_helpers import scrape_url
from utils.workflow_helpers import get_parallel_step_content, create_error_response, create_success_response


def scrape_vendor_homepage(step_input: StepInput) -> StepOutput:
    """
    Scrape vendor homepage.

    Args:
        step_input: StepInput with access to Step 1 validate_vendor output

    Returns:
        StepOutput with vendor homepage content (markdown, html, metadata)
    """
    try:
        # Get vendor validation data from parallel block (automatically deserializes)
        vendor_data = get_parallel_step_content(step_input, "parallel_validation", "validate_vendor")
        if not vendor_data:
            return create_error_response("Step 1 vendor validation failed: no data returned")

        # Type check - should be dict after deserialization
        if not isinstance(vendor_data, dict):
            return create_error_response(f"Step 1 vendor validation failed: expected dict, got {type(vendor_data).__name__}: {str(vendor_data)[:100]}")

        if "error" in vendor_data:
            return create_error_response(f"Step 1 vendor validation failed: {vendor_data['error']}")

        vendor_domain = vendor_data.get("vendor_domain")
        if not vendor_domain:
            return create_error_response("Step 1 vendor validation failed: no vendor_domain in data")

        print(f"📄 Scraping vendor homepage: {vendor_domain}")
        result = scrape_url(vendor_domain, formats=['markdown', 'html'])

        if not result.get("success"):
            error_msg = f"Failed to scrape vendor homepage: {result.get('error', 'Unknown error')}"
            return create_error_response(error_msg)

        markdown_content = result.get('markdown', '')
        print(f"✅ Scraped vendor homepage ({len(markdown_content)} chars)")

        return create_success_response({
            "vendor_domain": vendor_domain,
            "vendor_homepage_markdown": markdown_content,
            "vendor_homepage_html": result.get("html", ""),
            "vendor_homepage_metadata": result.get("metadata", {})
        })
    except Exception as e:
        return create_error_response(f"Error scraping vendor homepage: {str(e)}")


def scrape_prospect_homepage(step_input: StepInput) -> StepOutput:
    """
    Scrape prospect homepage.

    Args:
        step_input: StepInput with access to Step 1 validate_prospect output

    Returns:
        StepOutput with prospect homepage content (markdown, html, metadata)
    """
    try:
        # Get prospect validation data from parallel block (automatically deserializes)
        prospect_data = get_parallel_step_content(step_input, "parallel_validation", "validate_prospect")
        if not prospect_data:
            return create_error_response("Step 1 prospect validation failed: no data returned")

        # Type check - should be dict after deserialization
        if not isinstance(prospect_data, dict):
            return create_error_response(f"Step 1 prospect validation failed: expected dict, got {type(prospect_data).__name__}")

        if "error" in prospect_data:
            return create_error_response(f"Step 1 prospect validation failed: {prospect_data['error']}")

        prospect_domain = prospect_data.get("prospect_domain")
        if not prospect_domain:
            return create_error_response("Step 1 prospect validation failed: no prospect_domain in data")

        print(f"📄 Scraping prospect homepage: {prospect_domain}")
        result = scrape_url(prospect_domain, formats=['markdown', 'html'])

        if not result.get("success"):
            error_msg = f"Failed to scrape prospect homepage: {result.get('error', 'Unknown error')}"
            return create_error_response(error_msg)

        markdown_content = result.get('markdown', '')
        print(f"✅ Scraped prospect homepage ({len(markdown_content)} chars)")

        return create_success_response({
            "prospect_domain": prospect_domain,
            "prospect_homepage_markdown": markdown_content,
            "prospect_homepage_html": result.get("html", ""),
            "prospect_homepage_metadata": result.get("metadata", {})
        })
    except Exception as e:
        return create_error_response(f"Error scraping prospect homepage: {str(e)}")
