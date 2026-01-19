
# =========================================================
# TOOL META
# =========================================================
TOOL_NAME = "Software vs Hardware Requirement Review Tool"

BASE_INPUT = r"C:\Users\rprabhakargi\Downloads\review_2026\input"
BASE_OUTPUT = r"C:\Users\rprabhakargi\Downloads\review_2026\output"

SOFTWARE_REQ_FILE = "software_requirements.docx"
HARDWARE_DS_FILE  = "hardware_datasheet.docx"

DEFAULT_CPU_MHZ = 100
DEFAULT_RAM_KB = 128

SUPPORTED_INTERFACES = ["can", "spi", "uart", "i2c"]
UNSUPPORTED_INTERFACES = ["ethernet", "usb", "arinc", "pcie", "sata"]

TIMING_KEYWORDS = [
    "ms", "millisecond", "milliseconds",
    "us", "microsecond",
    "hz", "khz", "mhz",
    "period", "rate", "frequency",
    "latency", "deadline", "jitter",
]

COMMENTS = {
    "g31_hw_assumption": "Requirement assumes hardware capability not confirmed in target processor datasheet",
    "g31_cpu_load": "Computational complexity may exceed available CPU performance margin",
    "g31_not_justified": "Hardware constraints are not explicitly addressed or justified",
    "g32_no_timing": "Execution timing or rate is not specified",
    "g32_startup": "Startup or initialization timing is not defined",
    "g32_monitor": "Monitoring execution rate not defined",
    "g32_logging": "Logging frequency or execution rate is not specified",
    "g32_comm": "Communication timing requirements are missing",
    "g32_control": "Control loop execution timing not defined",
    "g33_unsupported_iface": "{} interface is not supported by the target hardware",
    "g33_no_bandwidth": "Interface usage specified without bandwidth or rate constraints",
    "g34_dynamic_memory": "Dynamic memory usage may violate determinism and certification guidelines",
    "g34_unbounded": "Unbounded or continuous operation specified without resource limits",
    "g34_resource_size": "Resource sizes are not explicitly bounded",
}
#################################
##g4####

# =========================================================
# G4 INPUT / OUTPUT
# =========================================================

G4_BASE_INPUT = r"C:\Users\rprabhakargi\Downloads\Review_Integration_2026\Input"
G4_OUTPUT_FILE = "CI_G4_output.xlsx"

# =========================================================
# G4 REGEX CONFIG
# =========================================================

VERIFICATION_METHOD_REGEX = (
    r"verification\s*method\s*:\s*"
    r"(Test|Analysis|Inspection|Demonstration|HSI|SI|Manual)"
)

MANDATORY_WORD_REGEX = r"\bshall\b"

# =========================================================
# G4 KEYWORD CONFIG
# =========================================================

REGISTER_KEYWORDS = [
    "register", "address", "bit", "offset"
]

COMMUNICATION_KEYWORDS = [
    "can", "uart", "spi", "i2c", "ethernet",
    "communication", "transmit", "receive"
]

FAULT_KEYWORDS = [
    "fault", "error", "failure", "detect",
    "report", "recovery", "diagnostic"
]

IO_KEYWORDS = [
    "input", "output", "gpio", "pin",
    "signal", "analog", "digital"
]

FUNCTIONAL_KEYWORDS = [
    "calculate", "compute", "process",
    "control", "manage", "monitor",
    "execute", "perform", "generate",
    "determine", "evaluate", "update",
    "initialize", "reset", "start", "stop",
    "schedule", "maintain", "handle"
]

# =========================================================
# G4 REQUIREMENT PREFIX
# =========================================================

REQ_PREFIX = "SCU_STC_SRS_"   # unchanged (logic preserved)
# =========================================================
# G5 INPUT / OUTPUT
# =========================================================

INPUT_SRS_FILE = "SCU_SRS.docx"
G5_OUTPUT_FILE = "SRS_Review_Report.xlsx"

# =========================================================
# G5 REQUIREMENT ID RULES
# =========================================================

EXPECTED_ID_PREFIX = "SCU_STC_SRS_"
VALID_ID_REGEX = r"^SCU_STC_SRS_\d+$"
MISSING_ID_LABEL = "<MISSING ID>"

# =========================================================
# G5 SAFETY CONFIG
# =========================================================

SAFETY_KEYWORDS = [
    "fault", "failure", "fail", "error", "loss", "hazard",
    "degraded", "safe state", "shutdown", "reset", "timeout",
    "monitor", "detect", "isolate", "protect", "recover",
    "invalid", "unsafe"
]

MITIGATION_KEYWORDS = [
    "detect", "prevent", "mitigate", "isolate", "monitor",
    "recover", "limit", "protect", "shutdown", "transition"
]

FORBIDDEN_SAFETY_PHRASES = [
    "best effort", "where possible", "if feasible",
    "normally", "typically", "as appropriate"
]

FORBIDDEN_MODALS = ["may", "should", "will"]

# =========================================================
# G5 AMBIGUOUS WORDS
# =========================================================

AMBIGUOUS_WORDS = [
    "should", "may", "might", "could",
    "normally", "typically", "as appropriate", "where possible"
]

# =========================================================
# G5 SINGLE FUNCTION CONFIG
# =========================================================

STOP_WORDS = {
    "SHALL", "WILL", "MAY", "PROGRAM", "SYSTEM", "WHEN", "IF",
    "THEN", "AND", "OR", "NOT", "ANY", "THE", "A", "AN",
    "LEVEL", "MODE", "STATE", "STATUS", "FAILSAFE", "MONITOR",
    "ACCORDING", "FOLLOWING", "CONFIRMATION", "LOGIC", "TIME",
    "WITH", "STC"
}

# =========================================================
# G5 EXCEL REPORT TEXT
# =========================================================

REPORT_TITLE = "High-Level requirements are conforms to standards"

COLUMN_HEADERS = [
    "Requirement ID",
    "5.1: Assess safety-critical aspects",
    "5.2: Ensure single functionality",
    "5.3: Follow project guidelines",
    "5.4: Avoid ambiguous words",
    "5.5: Check formatting & structure",
    "Failure Reason(s)"
]

# =========================
# G1 CONFIG
# =========================

# Uses SAME global input/output folders
G1_SRS_FILE = "SCU_SRS.docx"
G1_SES_FILE = "SCU_SES.docx"
G1_ICD_FILE = "SCU_ICD.docx"

# Runtime generated file (same input folder)
G1_SOFTWARE_REQ_DOCX = "Software_req.docx"

# Outputs (same output folder)
G1_3_OUTPUT_EXCEL = "G1_3_final_output.xlsx"
G1_4_OUTPUT_EXCEL = "G1_4_final_output.xlsx"

# Similarity thresholds (UNCHANGED)
SIM_MATCH = 0.85
SIM_POTENTIAL = 0.65

TERM_SYNONYMS = {
    "transmission interval": ["update rate", "refresh rate", "output rate"],
    "interface": ["bus", "port", "connection"],
    "signal": ["data", "parameter"],
    "receiver": ["destination", "sink"],
    "transmitter": ["source", "sender"],
}
# =========================================================
# COMMON REGEX (USED BY io_utils – DO NOT REMOVE)
# =========================================================

import re

REQ_ID_RE = re.compile(r"^(SCU_[A-Z_]+_\d+)\b")

LABEL_RE = re.compile(
    r"(?:label\s*(?:=|:)?\s*)?(\b\d{2,4}\b)",
    re.IGNORECASE
)
