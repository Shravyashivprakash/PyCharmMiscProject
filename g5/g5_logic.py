from g5.g5_1_logic import check_safety
from g5.g5_2_logic import check_single_functionality
from g5.g5_3_logic import check_project_guidelines
from g5.g5_4_logic import check_ambiguous_words
from g5.g5_5_logic import check_format_and_structure
from collections import defaultdict




def run_g5_checks(requirements):
    """
    Acts as the G5 aggregator.
    Calls all G5.x sub-guideline logic and combines results
    into a single G5 decision per requirement.
    """

    # ---------------------------
    # Run all sub-guidelines
    # ---------------------------
    g5_1_results = check_safety(requirements)
    g5_2_results = check_single_functionality(requirements)
    g5_3_results = check_project_guidelines(requirements)
    g5_4_results = check_ambiguous_words(requirements)
    g5_5_results = check_format_and_structure(requirements)

    # ---------------------------
    # Combine all findings
    # ---------------------------
    all_findings = (
        g5_1_results +
        g5_2_results +
        g5_3_results +
        g5_4_results +
        g5_5_results
    )

    # ---------------------------
    # Group by Requirement ID
    # ---------------------------
    findings_by_req = defaultdict(list)
    for req_id, issue in all_findings:
        findings_by_req[req_id].append(issue)

    # ---------------------------
    # Build final G5 result
    # ---------------------------
    g5_results = {}

    for req_id, issues in findings_by_req.items():
        g5_results[req_id] = {
            "overall": "FAIL" if issues else "PASS",
            "issues": issues
        }

    return g5_results, all_findings
