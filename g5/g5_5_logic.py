import re

from config import (
    EXPECTED_ID_PREFIX,
    VALID_ID_REGEX,
    MISSING_ID_LABEL
)


def first_two_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return " ".join(sentences[:2])


def check_format_and_structure(requirements):
    """
    Check formatting and structural correctness of requirements.
    """
    findings = []
    seen_ids = set()

    for req in requirements:
        raw_id = req.get("raw_id")
        req_id = req.get("id")
        text = req.get("text", "").strip()

        # FS-01: Missing requirement ID
        if not raw_id:
            preview = first_two_sentences(text)
            findings.append(
                (MISSING_ID_LABEL,
                 f"G_5.5-FS-01: Missing requirement ID\n    Preview: {preview}")
            )
            continue

        # FS-02: Invalid ID format
        if req_id is None and raw_id:
            preview = first_two_sentences(text)
            findings.append(
                (raw_id,
                 f"G_5.5-FS-02: Invalid requirement ID format\n    Preview: {preview}")
            )
            continue

        # FS-03: Duplicate requirement ID
        if req_id in seen_ids:
            findings.append(
                (req_id, "G_5.5-FS-03: Duplicate requirement ID")
            )
            continue

        seen_ids.add(req_id)

        # FS-04: Missing requirement text
        if not text:
            findings.append(
                (req_id, "G_5.5-FS-04: Requirement text is missing")
            )

    return findings
