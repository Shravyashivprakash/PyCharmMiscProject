# g1_4_logic.py
# ----------------------------------
import subprocess
import sys
import os

def run_g1_4(project_root):
    script = os.path.join(project_root, "G1_4_Requirement_Review.py")

    result = subprocess.run(
        [sys.executable, script],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return "G1.4 completed"
