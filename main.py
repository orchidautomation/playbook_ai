"""
Playbook AI - Main Entry Point
CLI for running the complete sales intelligence pipeline (all 4 phases).

Usage:
    python main.py <vendor_domain> <prospect_domain>

Examples (all formats accepted):
    python main.py gong.io sendoso.com
    python main.py https://gong.io https://sendoso.com
    python main.py www.gong.io www.sendoso.com

All domain formats are automatically normalized to https://

https://github.com/orchidautomation/playbook_ai-oss
"""

import sys
import json
import os
import time
from datetime import datetime, timedelta
from agno.workflow import Workflow, Step, Parallel
from models.workflow_input import WorkflowInput

# Import Phase 1 step executors
from steps.step1_domain_validation import validate_vendor_domain, validate_prospect_domain
from steps.step2_homepage_scraping import scrape_vendor_homepage, scrape_prospect_homepage
from steps.step3_initial_analysis import analyze_vendor_homepage, analyze_prospect_homepage
from steps.step4_url_prioritization import prioritize_urls
from steps.step5_batch_scraping import batch_scrape_selected_pages

# Import Phase 2 step executors (Step 6)
from steps.step6_vendor_extraction import (
    extract_offerings,
    extract_case_studies,
    extract_proof_points,
    extract_value_props,
    extract_customers,
    extract_use_cases,
    extract_personas,
    extract_differentiators
)

# Import Phase 3 step executors (Step 7)
from steps.step7_prospect_analysis import (
    analyze_company_profile,
    analyze_pain_points,
    identify_buyer_personas
)

# Import Phase 4 step executors (Step 8)
from steps.step8_playbook_generation import (
    generate_playbook_summary,
    generate_email_sequences,
    generate_talk_tracks,
    generate_battle_cards,
    assemble_final_playbook
)


# Complete Sales Intelligence Pipeline - All 4 Phases (8 Steps)
workflow = Workflow(
    name="Playbook AI - Sales Intelligence Pipeline",
    description="End-to-end: Intelligence, vendor extraction, prospect analysis, and actionable playbooks",
    input_schema=WorkflowInput,  # AgentOS API support with automatic domain normalization
    steps=[
        # Phase 1: Intelligence Gathering (Steps 1-5)

        # Step 1: Parallel domain validation
        Parallel(
            Step(name="validate_vendor", executor=validate_vendor_domain),
            Step(name="validate_prospect", executor=validate_prospect_domain),
            name="parallel_validation"
        ),

        # Step 2: Parallel homepage scraping
        Parallel(
            Step(name="scrape_vendor_home", executor=scrape_vendor_homepage),
            Step(name="scrape_prospect_home", executor=scrape_prospect_homepage),
            name="parallel_homepage_scraping"
        ),

        # Step 3: Parallel homepage analysis
        Parallel(
            Step(name="analyze_vendor_home", executor=analyze_vendor_homepage),
            Step(name="analyze_prospect_home", executor=analyze_prospect_homepage),
            name="parallel_homepage_analysis"
        ),

        # Step 4: URL prioritization
        Step(name="prioritize_urls", executor=prioritize_urls),

        # Step 5: Batch scraping
        Step(name="batch_scrape", executor=batch_scrape_selected_pages),

        # Phase 2: Vendor Extraction (Step 6)

        # Step 6: Vendor element extraction (8 parallel specialists)
        Parallel(
            Step(name="extract_offerings", executor=extract_offerings),
            Step(name="extract_case_studies", executor=extract_case_studies),
            Step(name="extract_proof_points", executor=extract_proof_points),
            Step(name="extract_value_props", executor=extract_value_props),
            Step(name="extract_customers", executor=extract_customers),
            Step(name="extract_use_cases", executor=extract_use_cases),
            Step(name="extract_personas", executor=extract_personas),
            Step(name="extract_differentiators", executor=extract_differentiators),
            name="vendor_element_extraction"
        ),

        # Phase 3: Prospect Analysis (Step 7)

        # Step 7a: Prospect context analysis (2 parallel analysts)
        Parallel(
            Step(name="analyze_company", executor=analyze_company_profile),
            Step(name="analyze_pain_points", executor=analyze_pain_points),
            name="prospect_context_analysis"
        ),

        # Step 7b: Buyer persona identification (uses vendor + prospect data)
        Step(name="identify_buyer_personas", executor=identify_buyer_personas),

        # Phase 4: Playbook Generation (Step 8)

        # Step 8a: Playbook summary (sequential - needs all Phase 1-3 data)
        Step(name="generate_playbook_summary", executor=generate_playbook_summary),

        # Step 8b-d: Playbook components (3 parallel specialists)
        Parallel(
            Step(name="generate_email_sequences", executor=generate_email_sequences),
            Step(name="generate_talk_tracks", executor=generate_talk_tracks),
            Step(name="generate_battle_cards", executor=generate_battle_cards),
            name="playbook_component_generation"
        ),

        # Step 8e: Final playbook assembly
        Step(name="assemble_final_playbook", executor=assemble_final_playbook)
    ]
)


def main():
    """Main entry point for complete sales intelligence pipeline."""

    # Parse command line arguments
    if len(sys.argv) < 3:
        print("=" * 80)
        print("PLAYBOOK AI - SALES INTELLIGENCE PIPELINE")
        print("=" * 80)
        print("\nUsage: python main.py <vendor_domain> <prospect_domain>")
        print("\nExamples (all formats work):")
        print("  python main.py gong.io sendoso.com")
        print("  python main.py https://gong.io https://sendoso.com")
        print("  python main.py www.gong.io www.sendoso.com")
        print("\nThis runs all 4 phases:")
        print("  Phase 1: Intelligence Gathering (Steps 1-5)")
        print("  Phase 2: Vendor GTM Extraction (Step 6)")
        print("  Phase 3: Prospect Analysis (Step 7)")
        print("  Phase 4: Sales Playbook Generation (Step 8)")
        print("\n" + "=" * 80)
        sys.exit(1)

    # Normalize domains using Pydantic validation
    # This accepts flexible inputs: sendoso.com, www.sendoso.com, https://sendoso.com
    try:
        validated_input = WorkflowInput(
            vendor_domain=sys.argv[1],
            prospect_domain=sys.argv[2]
        )
        vendor_domain = validated_input.vendor_domain
        prospect_domain = validated_input.prospect_domain
    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ INVALID DOMAIN INPUT")
        print("=" * 80)
        print(f"\nError: {str(e)}")
        print("\nPlease provide valid domain names.")
        print("\nExamples:")
        print("  python main.py gong.io sendoso.com")
        print("  python main.py https://gong.io https://sendoso.com")
        print("=" * 80)
        sys.exit(1)

    # Display header
    print("\n" + "=" * 80)
    print("PLAYBOOK AI - SALES INTELLIGENCE PIPELINE")
    print("=" * 80)
    print(f"\n📊 Vendor:   {vendor_domain}")
    print(f"🎯 Prospect: {prospect_domain}\n")
    print("=" * 80)
    print("\n🚀 Starting Complete Workflow (All 4 Phases)...")
    print("   Phase 1: Intelligence Gathering")
    print("   Phase 2: Vendor GTM Extraction")
    print("   Phase 3: Prospect Analysis")
    print("   Phase 4: Sales Playbook Generation")
    print("\n" + "=" * 80 + "\n")

    # Prepare workflow input
    workflow_input = {
        "vendor_domain": vendor_domain,
        "prospect_domain": prospect_domain
    }

    try:
        # Capture start time for duration tracking
        start_time = time.time()

        # Run workflow with streaming (single execution)
        print("🔥 Workflow executing with real-time visualization...\n")
        response_stream = workflow.run(input=workflow_input, stream=True)

        # Process stream events and get final result
        result = None
        for event in response_stream:
            # The stream displays automatically via Agno's TUI
            # Last event is the final WorkflowRunOutput
            result = event

        # Check if workflow was successful
        if not result or not result.content:
            print("\n" + "=" * 80)
            print("❌ WORKFLOW FAILED")
            print("=" * 80)
            print("\nNo result returned from workflow.")
            sys.exit(1)

        # Helper functions to extract step content from WorkflowCompletedEvent
        def get_step_content_by_name(step_results, step_name):
            """Find and return content from a step by name"""
            for step_output in step_results:
                if step_output.step_name == step_name:
                    return step_output.content
            return None

        def get_parallel_substep_content(step_results, parallel_step_name, substep_name):
            """Extract content from a specific substep within a parallel step"""
            for step_output in step_results:
                if step_output.step_name == parallel_step_name and step_output.step_type == "Parallel":
                    if hasattr(step_output, 'steps') and step_output.steps:
                        for sub_step in step_output.steps:
                            if sub_step.step_name == substep_name:
                                return sub_step.content
            return None

        # Calculate duration
        end_time = time.time()
        duration_seconds = round(end_time - start_time, 2)

        # Create timestamp and run directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = f"output/runs/{timestamp}"
        os.makedirs(run_dir, exist_ok=True)

        # Create research subdirectories (consolidated structure)
        vendor_dir = f"{run_dir}/research/vendor"
        prospect_dir = f"{run_dir}/research/prospect"
        os.makedirs(vendor_dir, exist_ok=True)
        os.makedirs(prospect_dir, exist_ok=True)

        # === EXTRACT ALL STEP CONTENT ===

        # Step 6: Vendor extraction (8 extractors)
        offerings = get_parallel_substep_content(result.step_results, "vendor_element_extraction", "extract_offerings") or {}
        case_studies = get_parallel_substep_content(result.step_results, "vendor_element_extraction", "extract_case_studies") or {}
        proof_points = get_parallel_substep_content(result.step_results, "vendor_element_extraction", "extract_proof_points") or {}
        value_props = get_parallel_substep_content(result.step_results, "vendor_element_extraction", "extract_value_props") or {}
        customers = get_parallel_substep_content(result.step_results, "vendor_element_extraction", "extract_customers") or {}
        use_cases = get_parallel_substep_content(result.step_results, "vendor_element_extraction", "extract_use_cases") or {}
        personas = get_parallel_substep_content(result.step_results, "vendor_element_extraction", "extract_personas") or {}
        differentiators = get_parallel_substep_content(result.step_results, "vendor_element_extraction", "extract_differentiators") or {}

        # Step 7: Prospect analysis (3 analysts)
        company_profile = get_parallel_substep_content(result.step_results, "prospect_context_analysis", "analyze_company") or {}
        pain_points = get_parallel_substep_content(result.step_results, "prospect_context_analysis", "analyze_pain_points") or {}
        buyer_personas = get_step_content_by_name(result.step_results, "identify_buyer_personas") or {}

        # Step 8: Playbook generation (5 components)
        playbook_summary = get_step_content_by_name(result.step_results, "generate_playbook_summary") or {}
        email_sequences = get_parallel_substep_content(result.step_results, "playbook_component_generation", "generate_email_sequences") or {}
        talk_tracks = get_parallel_substep_content(result.step_results, "playbook_component_generation", "generate_talk_tracks") or {}
        battle_cards = get_parallel_substep_content(result.step_results, "playbook_component_generation", "generate_battle_cards") or {}
        final_playbook = get_step_content_by_name(result.step_results, "assemble_final_playbook") or {}

        # === SAVE CONSOLIDATED FILES ===

        # 1. Vendor Research Files (5 files, consolidated from 8)

        # offerings.json - keep as-is
        with open(f"{vendor_dir}/offerings.json", "w") as f:
            json.dump(offerings, f, indent=2)

        # customer_evidence.json - merge: case_studies + proof_points + customers
        customer_evidence = {
            "case_studies": case_studies.get("case_studies", []) if isinstance(case_studies, dict) else [],
            "proof_points": proof_points.get("proof_points", []) if isinstance(proof_points, dict) else [],
            "customers": customers.get("customers", []) if isinstance(customers, dict) else []
        }
        with open(f"{vendor_dir}/customer_evidence.json", "w") as f:
            json.dump(customer_evidence, f, indent=2)

        # positioning.json - merge: differentiators + value_props
        positioning = {
            "differentiators": differentiators.get("differentiators", []) if isinstance(differentiators, dict) else [],
            "value_propositions": value_props.get("value_propositions", []) if isinstance(value_props, dict) else []
        }
        with open(f"{vendor_dir}/positioning.json", "w") as f:
            json.dump(positioning, f, indent=2)

        # personas.json - keep as-is
        with open(f"{vendor_dir}/personas.json", "w") as f:
            json.dump(personas, f, indent=2)

        # use_cases.json - keep as-is
        with open(f"{vendor_dir}/use_cases.json", "w") as f:
            json.dump(use_cases, f, indent=2)

        # 2. Prospect Research Files (1 file, consolidated from 3)

        # analysis.json - merge: company_profile + pain_points + buyer_personas
        prospect_analysis = {
            "company_profile": company_profile.get("company_profile", company_profile) if isinstance(company_profile, dict) else {},
            "pain_points": pain_points.get("pain_points", []) if isinstance(pain_points, dict) else [],
            "buyer_personas": buyer_personas.get("target_buyer_personas", []) if isinstance(buyer_personas, dict) else []
        }
        with open(f"{prospect_dir}/analysis.json", "w") as f:
            json.dump(prospect_analysis, f, indent=2)

        # 3. Main Playbook (1 file - merge playbook_summary + final_playbook)

        playbook = {}

        # From playbook_summary - strategic context and intelligence
        if isinstance(playbook_summary, dict):
            playbook["executive_summary"] = playbook_summary.get("executive_summary", "")
            playbook["priority_personas"] = playbook_summary.get("priority_personas", [])
            playbook["quick_wins"] = playbook_summary.get("quick_wins", [])
            playbook["success_metrics"] = playbook_summary.get("success_metrics", {})
            playbook["vendor_intelligence"] = playbook_summary.get("vendor_intelligence", {})
            playbook["prospect_intelligence"] = playbook_summary.get("prospect_intelligence", {})

        # From final_playbook - tactical content
        if isinstance(final_playbook, dict):
            sales_playbook = final_playbook.get("sales_playbook", {})
            playbook["vendor_name"] = sales_playbook.get("vendor_name", "")
            playbook["prospect_name"] = sales_playbook.get("prospect_name", "")
            playbook["generated_date"] = sales_playbook.get("generated_date", timestamp[:8])
            playbook["email_sequences"] = sales_playbook.get("email_sequences", [])
            playbook["talk_tracks"] = sales_playbook.get("talk_tracks", [])
            playbook["battle_cards"] = sales_playbook.get("battle_cards", [])

        with open(f"{run_dir}/playbook.json", "w") as f:
            json.dump(playbook, f, indent=2)

        # 4. Enhanced Metadata

        metadata = {
            "run_id": timestamp,
            "timestamp_start": (datetime.now() - timedelta(seconds=duration_seconds)).isoformat(),
            "timestamp_end": datetime.now().isoformat(),
            "duration_seconds": duration_seconds,
            "workflow_name": workflow.name,
            "workflow_version": "2.0.0",
            "status": "completed",
            "inputs": {
                "vendor_domain": vendor_domain,
                "prospect_domain": prospect_domain
            },
            "outputs": {
                "vendor_name": playbook.get("vendor_name", ""),
                "prospect_name": playbook.get("prospect_name", ""),
                "persona_count": len(playbook.get("priority_personas", [])),
                "email_sequence_count": len(playbook.get("email_sequences", [])),
                "talk_track_count": len(playbook.get("talk_tracks", [])),
                "battle_card_count": len(playbook.get("battle_cards", []))
            },
            "file_manifest": {
                "playbook": "playbook.json",
                "research": {
                    "vendor": [
                        "research/vendor/offerings.json",
                        "research/vendor/customer_evidence.json",
                        "research/vendor/positioning.json",
                        "research/vendor/personas.json",
                        "research/vendor/use_cases.json"
                    ],
                    "prospect": [
                        "research/prospect/analysis.json"
                    ]
                }
            }
        }

        with open(f"{run_dir}/metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        # === DISPLAY SUCCESS MESSAGE ===

        print("\n" + "=" * 80)
        print("✅ COMPLETE WORKFLOW FINISHED!")
        print("=" * 80)

        print(f"\n📁 Outputs saved to: {run_dir}/")
        print(f"   • playbook.json - Complete sales playbook (USE THIS)")
        print(f"   • metadata.json - Run information and stats")
        print(f"   • research/vendor/ - Raw vendor intelligence (5 files)")
        print(f"   • research/prospect/ - Raw prospect analysis (1 file)")

        print(f"\n⏱️  Duration: {duration_seconds:.1f} seconds")

        print(f"\n📊 Playbook Stats:")
        print(f"   • Vendor: {playbook.get('vendor_name', 'Unknown')}")
        print(f"   • Prospect: {playbook.get('prospect_name', 'Unknown')}")
        print(f"   • Personas: {len(playbook.get('priority_personas', []))}")
        print(f"   • Email sequences: {len(playbook.get('email_sequences', []))}")
        print(f"   • Talk tracks: {len(playbook.get('talk_tracks', []))}")
        print(f"   • Battle cards: {len(playbook.get('battle_cards', []))}")

        print("\n" + "=" * 80)
        print("🎉 All phases complete! Sales playbook ready.")
        print("=" * 80 + "\n")

    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ WORKFLOW ERROR")
        print("=" * 80)
        print(f"\nError: {str(e)}")
        print("\nPlease check your API keys in .env and try again.")
        print("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()
