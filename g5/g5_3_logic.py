import re

SUBJECT_PREFIX = "the stc program shall"

FORBIDDEN_MODALS = ["must", "will", "should", "may"]
FORBIDDEN_VAGUE = [
    "etc",
    "as appropriate",
    "as required",
    "as needed",
    "adequate",
    "sufficient"
]

PASSIVE_PATTERNS = [
    r"shall be provided",
    r"shall be handled",
    r"shall be performed",
    r"shall be supported"
]


def check_project_guidelines(requirements):
    findings = []

    for req in requirements:
        req_id = req.get("id")
        text = req.get("text", "").strip()

        # Skip rows without valid ID (already handled elsewhere)
        if not req_id or not text:
            continue

        text_lower = text.lower()

        # PG-01: Must contain "shall"
        if "shall" not in text_lower:
            findings.append((req_id, "G_5.3-PG-01: Requirement does not contain 'shall'"))

        # PG-02: Exactly one "shall"
        if text_lower.count("shall") > 1:
            findings.append((req_id, "G_5.3-PG-02: Multiple 'shall' statements found"))

        # PG-03: Must start with subject
        if not text_lower.startswith(SUBJECT_PREFIX):
            findings.append(
                (req_id, "G_5.3-PG-03: Requirement does not start with 'The STC Program shall'")
            )

        # PG-04: Forbidden modal verbs
        for word in FORBIDDEN_MODALS:
            if re.search(rf"\b{word}\b", text_lower):
                findings.append(
                    (req_id, f"G_5.3-PG-04: Forbidden modal verb used ('{word}')")
                )

        # PG-05: Forbidden vague words
        for phrase in FORBIDDEN_VAGUE:
            if phrase in text_lower:
                findings.append(
                    (req_id, f"G_5.3-PG-05: Forbidden vague term used ('{phrase}')")
                )

        # PG-06: Basic passive voice detection
        for pattern in PASSIVE_PATTERNS:
            if re.search(pattern, text_lower):
                findings.append(
                    (req_id, "G_5.3-PG-06: Possible passive voice usage")
                )

    return findings
