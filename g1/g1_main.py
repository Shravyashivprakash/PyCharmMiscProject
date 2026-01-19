import os
import pandas as pd

from config import (
    BASE_INPUT,
    BASE_OUTPUT,
    G1_SRS_FILE,
    G1_SES_FILE,
    G1_3_OUTPUT_EXCEL,
    G1_4_OUTPUT_EXCEL
)

from io_utils import extract_docx_text, extract_requirements
from g1.g1_logic import compare_g1_3, check_g1


def run_g1():
    print(">>> G1 review started")

    # ---------- G1.3 ----------
    msg_cmp, rx_cmp = compare_g1_3()

    with pd.ExcelWriter(os.path.join(BASE_OUTPUT, G1_3_OUTPUT_EXCEL),
                        engine="openpyxl") as w:
        pd.DataFrame(msg_cmp).to_excel(w, "Message_Definition", index=False)
        pd.DataFrame(rx_cmp).to_excel(w, "Rx_Rate", index=False)

    # ---------- G1.4 ----------
    hlr_text = extract_docx_text(os.path.join(BASE_INPUT, G1_SRS_FILE))
    sys_text = extract_docx_text(os.path.join(BASE_INPUT, G1_SES_FILE))

    hlr_reqs = extract_requirements(hlr_text)
    sys_reqs = extract_requirements(sys_text)

    rows = []
    for hid, htxt in hlr_reqs.items():
        rows.append([hid, *check_g1(hid, htxt, sys_reqs)])

    df = pd.DataFrame(rows, columns=[
        "HLR ID", "Mapped System Req", "Label Match",
        "Terminology", "Intent Similarity", "Overall Status"
    ])

    df.to_excel(os.path.join(BASE_OUTPUT, G1_4_OUTPUT_EXCEL), index=False)

    print("<<< G1 review completed")
