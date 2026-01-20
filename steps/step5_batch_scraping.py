"""
Step 5: Batch Scraping
Batch scrapes all selected URLs from vendor and prospect websites.
Sequential step (runs after URL prioritization).
"""

from agno.workflow.types import StepInput, StepOutput
from utils.firecrawl_helpers import batch_scrape_urls
from utils.workflow_helpers import validate_previous_step_data, create_error_response, create_success_response
import config


def batch_scrape_selected_pages(step_input: StepInput) -> StepOutput:
    """
    Batch scrape all selected URLs from vendor and prospect.

    Args:
        step_input: StepInput with access to Step 4 prioritize_urls output

    Returns:
        StepOutput with scraped content separated by vendor/prospect
    """
    # Get selected URLs from Step 4
    is_valid, url_data, error_msg = validate_previous_step_data(
        step_input,
        required_keys=["vendor_selected_urls", "prospect_selected_urls"],
        step_name="Step 4 (URL prioritization)"
    )

    if not is_valid:
        return create_error_response(error_msg)

    vendor_urls = url_data.get("vendor_selected_urls", [])
    prospect_urls = url_data.get("prospect_selected_urls", [])

    # Combine and limit total URLs
    all_urls = vendor_urls + prospect_urls

    if len(all_urls) > config.MAX_URLS_TO_SCRAPE:
        print(f"⚠️  Too many URLs ({len(all_urls)}), limiting to {config.MAX_URLS_TO_SCRAPE}")
        # Take proportionally from each
        vendor_limit = int(config.MAX_URLS_TO_SCRAPE * len(vendor_urls) / len(all_urls))
        prospect_limit = config.MAX_URLS_TO_SCRAPE - vendor_limit
        vendor_urls = vendor_urls[:vendor_limit]
        prospect_urls = prospect_urls[:prospect_limit]
        all_urls = vendor_urls + prospect_urls

    print(f"📚 Batch scraping {len(all_urls)} URLs ({len(vendor_urls)} vendor + {len(prospect_urls)} prospect)...")
    print(f"⏱️  This may take up to {config.BATCH_SCRAPE_TIMEOUT} seconds...")

    try:
        # Batch scrape
        result = batch_scrape_urls(all_urls, formats=['markdown'])

        if not result["success"]:
            error_msg = f"Batch scraping failed: {result.get('error', 'Unknown error')}"
            return create_error_response(error_msg)

        scraped_results = result["results"]

        # Separate vendor and prospect content
        vendor_content = {}
        prospect_content = {}

        for url, data in scraped_results.items():
            markdown = data.get("markdown", "")
            if not markdown:
                print(f"    Warning: No markdown content for {url}")
                continue
            if url in vendor_urls:
                vendor_content[url] = markdown
            elif url in prospect_urls:
                prospect_content[url] = markdown

        print(f"✅ Scraped {len(vendor_content)} vendor pages and {len(prospect_content)} prospect pages")

        # Calculate total content size
        total_vendor_chars = sum(len(content) for content in vendor_content.values())
        total_prospect_chars = sum(len(content) for content in prospect_content.values())

        print(f"📊 Vendor content: {total_vendor_chars:,} characters")
        print(f"📊 Prospect content: {total_prospect_chars:,} characters")

        return create_success_response({
            "vendor_content": vendor_content,
            "prospect_content": prospect_content,
            "vendor_urls_scraped": list(vendor_content.keys()),
            "prospect_urls_scraped": list(prospect_content.keys()),
            "total_scraped": len(scraped_results),
            "stats": {
                "vendor_pages": len(vendor_content),
                "prospect_pages": len(prospect_content),
                "vendor_chars": total_vendor_chars,
                "prospect_chars": total_prospect_chars
            }
        })

    except Exception as e:
        return create_error_response(f"Batch scraping failed: {str(e)}")
