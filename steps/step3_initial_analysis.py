"""
Step 3: Initial Analysis
Analyzes vendor and prospect homepages using AI.
Runs in parallel for both homepages.
"""

from agno.workflow.types import StepInput, StepOutput
from agents.homepage_analyst import homepage_analyst
from utils.workflow_helpers import get_parallel_step_content, create_error_response, create_success_response


def analyze_vendor_homepage(step_input: StepInput) -> StepOutput:
    """
    Analyze vendor homepage with AI.

    Args:
        step_input: StepInput with access to Step 2 parallel_homepage_scraping output

    Returns:
        StepOutput with vendor homepage analysis
    """
    # Get vendor homepage data from parallel block
    vendor_homepage_data = get_parallel_step_content(step_input, "parallel_homepage_scraping", "scrape_vendor_home")

    if not vendor_homepage_data or "error" in vendor_homepage_data:
        return create_error_response(f"Step 2 vendor scraping failed: {vendor_homepage_data.get('error', 'no data returned')}")

    markdown_content = vendor_homepage_data.get("vendor_homepage_markdown", "")

    if not markdown_content or len(markdown_content) < 100:
        return create_error_response("Vendor homepage content is too short or empty")

    print(f"🤖 Analyzing vendor homepage with AI...")

    try:
        response = homepage_analyst.run(
            input=f"Analyze this homepage:\n\n{markdown_content}"
        )

        print(f"✅ Vendor homepage analyzed")

        return create_success_response({
            "vendor_homepage_analysis": response.content
        })

    except Exception as e:
        return create_error_response(f"AI analysis failed ({type(e).__name__}): {str(e)}")


def analyze_prospect_homepage(step_input: StepInput) -> StepOutput:
    """
    Analyze prospect homepage with AI.

    Args:
        step_input: StepInput with access to Step 2 parallel_homepage_scraping output

    Returns:
        StepOutput with prospect homepage analysis
    """
    # Get prospect homepage data from parallel block
    prospect_homepage_data = get_parallel_step_content(step_input, "parallel_homepage_scraping", "scrape_prospect_home")

    if not prospect_homepage_data or "error" in prospect_homepage_data:
        return create_error_response(f"Step 2 prospect scraping failed: {prospect_homepage_data.get('error', 'no data returned')}")

    markdown_content = prospect_homepage_data.get("prospect_homepage_markdown", "")

    if not markdown_content or len(markdown_content) < 100:
        return create_error_response("Prospect homepage content is too short or empty")

    print(f"🤖 Analyzing prospect homepage with AI...")

    try:
        response = homepage_analyst.run(
            input=f"Analyze this homepage:\n\n{markdown_content}"
        )

        print(f"✅ Prospect homepage analyzed")

        return create_success_response({
            "prospect_homepage_analysis": response.content
        })

    except Exception as e:
        return create_error_response(f"AI analysis failed ({type(e).__name__}): {str(e)}")
