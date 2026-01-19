import re
from config import STOP_WORDS
ENTITY_REGEX = re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")


# =========================
# Helpers
# =========================

def extract_entities(text: str) -> set:
    candidates = ENTITY_REGEX.findall(text.upper())

    filtered = set()
    for c in candidates:
        # Keep only meaningful functional entities
        if (
            "_" in c or
            re.search(r"\d$", c)
        ) and c not in STOP_WORDS:
            filtered.add(c)

    return filtered


def count_shall(text: str) -> int:
    return len(re.findall(r"\bshall\b", text, re.IGNORECASE))


def extract_shall_clause(text: str) -> str:
    match = re.search(r"(.*?\bshall\b.*?)(\.|\n)",
                      text, re.IGNORECASE | re.DOTALL)
    return match.group(1) if match else text


def extract_write_targets(text: str) -> set:
    targets = set()
    for line in text.splitlines():
        if "=" in line:
            lhs = line.split("=", 1)[0]
            targets |= extract_entities(lhs)
    return targets


def is_derived_entity(scope: str, target: str) -> bool:
    return scope in target


# =========================
# Main Check
# =========================

def check_single_functionality(requirements):
    findings = []

    for req in requirements:
        req_id = req.get("id")
        text = req.get("text", "")

        if not req_id or not text:
            continue

        # -------------------------
        # Rule 1: Multiple SHALL
        # -------------------------
        shall_count = count_shall(text)
        if shall_count > 1:
            findings.append((
                req_id,
                "G_5.2: Single functionality violation.\n"
                f"Reason: The requirement contains {shall_count} 'shall' "
                "statements, which indicates multiple system behaviors."
            ))
            continue

        # -------------------------
        # Rule 2: Scope entity
        # -------------------------
        shall_clause = extract_shall_clause(text)
        scope_entities = extract_entities(shall_clause)

        if not scope_entities:
            continue

        # -------------------------
        # Rule 3: Write targets
        # -------------------------
        write_targets = extract_write_targets(text)
        if not write_targets:
            continue

        # -------------------------
        # Explicit multi-entity PASS
        # -------------------------
        if len(scope_entities) > 1 and write_targets.issubset(scope_entities):
            continue

        # -------------------------
        # Derived entity allowance
        # -------------------------
        allowed_targets = {
            t for t in write_targets
            for s in scope_entities
            if is_derived_entity(s, t)
        }

        illegal_targets = write_targets - scope_entities - allowed_targets

        if illegal_targets:
            findings.append((
                req_id,
                "G_5.2: Single functionality violation.\n"
                f"Reason: This requirement defines behavior for "
                f"{', '.join(sorted(scope_entities))}, but assigns values to "
                f"{', '.join(sorted(illegal_targets))}. "
                "Writing to a different functional entity introduces "
                "multiple functionalities in a single requirement."
            ))

    return findings
