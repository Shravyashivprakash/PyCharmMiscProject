import math
from collections import Counter

from config import SIM_MATCH, SIM_POTENTIAL, TERM_SYNONYMS
from io_utils import norm, parse_bits, extract_labels
from g1.g1_3_logic import (
    generate_software_req,
    extract_srs_arinc,
    extract_icd_arinc
)


def compare_g1_3():
    generate_software_req()

    srs_rx, srs_msg = extract_srs_arinc()
    icd_rx, icd_msg = extract_icd_arinc()

    msg_out, rx_out = [], []

    for s in srs_msg:
        match = next(
            (i for i in icd_msg if i["Label"] == s["Label"]
             and norm(i["Field"]) == norm(s["Field"])),
            None
        )

        if not match:
            msg_out.append({**s, "Status": "Fail", "Reason": "Field not found in ICD"})
            continue

        sb1, _ = parse_bits(s["Bit"])
        ib1, _ = parse_bits(match["Bit"])

        fails = []
        if sb1 != (ib1 + 1 if ib1 is not None else None):
            fails.append("Bit offset mismatch (SRS = ICD + 1)")
        if norm(s["Description"]) != norm(match["Description"]):
            fails.append("Description mismatch")
        if norm(s["Definition"]) != norm(match["Definition"]):
            fails.append("Definition mismatch")

        msg_out.append({
            **s,
            "ICD Bit": match["Bit"],
            "Status": "Pass" if not fails else "Fail",
            "Reason": " | ".join(fails)
        })

    for s in srs_rx:
        match = next(
            (i for i in icd_rx if i["Label"] == s["Label"]
             and norm(i["Receiver"]) == norm(s["Receiver"])),
            None
        )

        if not match:
            rx_out.append({**s, "Status": "Fail", "Reason": "Receiver not found in ICD"})
            continue

        ok = norm(s["Interval"]) == norm(match["Interval"])
        rx_out.append({
            **s,
            "ICD Interval": match["Interval"],
            "Status": "Pass" if ok else "Fail",
            "Reason": "" if ok else "Transmission interval mismatch"
        })

    return msg_out, rx_out


def cosine_similarity(a, b):
    c1, c2 = Counter(a.split()), Counter(b.split())
    inter = set(c1) & set(c2)
    num = sum(c1[x] * c2[x] for x in inter)
    den = math.sqrt(sum(v*v for v in c1.values()) * sum(v*v for v in c2.values()))
    return num / den if den else 0.0


def find_best_sys_req(hlr_text, sys_reqs):
    hlr_labels = extract_labels(hlr_text)

    for sid, stext in sys_reqs.items():
        if hlr_labels & extract_labels(stext):
            sim = cosine_similarity(hlr_text, stext)
            return sid, stext, max(sim, SIM_POTENTIAL), True

    best = (None, None, 0.0, False)
    for sid, stext in sys_reqs.items():
        sim = cosine_similarity(hlr_text, stext)
        if sim >= SIM_POTENTIAL and sim > best[2]:
            best = (sid, stext, sim, False)

    return best


def check_g1(hlr_id, hlr_text, sys_reqs):
    sid, stxt, sim, label_match = find_best_sys_req(hlr_text, sys_reqs)

    if not sid:
        return ("Mapping not present", "No", "Mismatch", 0.0,
                "Fail" if hlr_id == "SCU_STC_SRS_1038" else "Review Required")

    intent = "Match" if sim > SIM_MATCH else "Mismatch"
    overall = "Pass" if intent == "Match" else "Review Required"

    return sid, "Yes" if label_match else "No", "Match", round(sim, 3), overall
