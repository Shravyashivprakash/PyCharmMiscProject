import os
import re
import datetime
from openpyxl import Workbook

from config import (
    BASE_INPUT,
    BASE_OUTPUT,
    SOFTWARE_REQ_FILE,
    HARDWARE_DS_FILE,
    DEFAULT_CPU_MHZ,
    DEFAULT_RAM_KB,
    SUPPORTED_INTERFACES,
    UNSUPPORTED_INTERFACES,
)

from io_utils import read_all_text
from g3.g3_logic import check_g3


def run_g3():
    # ---- Read hardware ----
    hw_text = " ".join(
        read_all_text(os.path.join(BASE_INPUT, HARDWARE_DS_FILE))
    ).lower()

    hardware = {
        "cpu_mhz": DEFAULT_CPU_MHZ,
        "ram_kb": DEFAULT_RAM_KB,
        "external_memory": "external memory" in hw_text,
        "supported_ifaces": SUPPORTED_INTERFACES,
        "unsupported_ifaces": UNSUPPORTED_INTERFACES,
    }

    # ---- Read software requirements ----
    full_text = "\n".join(
        read_all_text(os.path.join(BASE_INPUT, SOFTWARE_REQ_FILE))
    )

    parts = re.split(r"(SCU[_\- ]STC[_\- ]SRS[_\- ]\d+)", full_text)

    requirements = []
    for i in range(1, len(parts), 2):
        rid = parts[i].replace(" ", "_").replace("-", "_")
        rtext = parts[i + 1] if i + 1 < len(parts) else ""
        requirements.append((rid, rtext))

    # ---- Excel ----
    wb = Workbook()
    ws = wb.active
    ws.append(["Requirement ID", "G3.1", "G3.2", "G3.3", "G3.4", "Comment"])

    for rid, rtext in requirements:
        ws.append([rid, *check_g3(rtext, hardware)])

    os.makedirs(BASE_OUTPUT, exist_ok=True)
    out = os.path.join(
        BASE_OUTPUT,
        f"G3_Review_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
    )
    wb.save(out)

    print("Generated:", out)
