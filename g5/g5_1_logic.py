import re

from config import (
    SAFETY_KEYWORDS,
    MITIGATION_KEYWORDS,
    FORBIDDEN_SAFETY_PHRASES,
    FORBIDDEN_MODALS
)


def is_safety_related(text_lower):
    """
    Identify whether a requirement is safety-related
    based on presence of safety keywords.
    """
    return any(keyword in text_lower for keyword in SAFETY_KEYWORDS)


def check_safety(requirements):
    """
    Perform safety-related checks on requirements.

    Implements:
    SR-01: Must include mitigation strategy
    SR-02: Must describe system reaction
    SR-03: Must not use vague phrases
    SR-04: Must not use forbidden modal verbs
    """
    findings = []

    for req in requirements:
        req_id = req.get("id")
        text = req.get("text", "").strip()

        if not req_id or not text:
            continue

        text_lower = text.lower()

        # Step 1: Identify safety-related requirement
        if not is_safety_related(text_lower):
            continue  # Not a safety requirement

        # -------------------------------
        # SR-01: Must include mitigation
        # -------------------------------
        if not any(word in text_lower for word in MITIGATION_KEYWORDS):
            findings.append((
                req_id,
                "G_5.1-SR-01: No mitigation action found.\n"
                "Reason: The requirement mentions a safety concern but does not specify "
                "what the system shall do to prevent, control, or reduce the hazard."
            ))

        # ----------------------------------------
        # SR-02: Must describe system reaction
        # ----------------------------------------
        if not re.search(r"\bshall\s+\w+", text_lower):
            findings.append((
                req_id,
                "G_5.1-SR-02: Missing system behavior.\n"
                "Reason: The requirement does not contain a clear 'shall <action>' "
                "statement describing how the system responds to the condition."
            ))

        # ----------------------------------------
        # SR-03: Forbidden vague phrases
        # ----------------------------------------
        for phrase in FORBIDDEN_SAFETY_PHRASES:
            if phrase in text_lower:
                findings.append((
                    req_id,
                    f"G_5.1-SR-03: Vague safety wording detected ('{phrase}').\n"
                    f"Reason: The phrase '{phrase}' makes the behavior non-verifiable."
                ))

        # ----------------------------------------
        # SR-04: Forbidden modal verbs
        # ----------------------------------------
        for modal in FORBIDDEN_MODALS:
            if re.search(rf"\b{modal}\b", text_lower):
                findings.append((
                    req_id,
                    f"G_5.1-SR-04: Weak modal verb used ('{modal}').\n"
                    f"Reason: Safety requirements must use 'shall' instead of '{modal}' "
                    "to ensure the behavior is mandatory and testable."
                ))

    return findings
