from config import AMBIGUOUS_WORDS


def check_ambiguous_words(requirements):
    """
    Check for ambiguous or non-mandatory words in requirements.
    """
    findings = []

    for req in requirements:
        req_id = req.get("id")
        text = req.get("text", "").strip()

        if not req_id or not text:
            continue

        text_lower = text.lower()

        for word in AMBIGUOUS_WORDS:
            if word in text_lower:
                findings.append(
                    (req_id, f"G_5.4-AW-01: Ambiguous word used ('{word}')")
                )

    return findings
