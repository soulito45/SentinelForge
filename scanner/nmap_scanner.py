import subprocess
import tempfile
import xml.etree.ElementTree as ET


def run_nmap(target: str) -> str:
    """
    Run a conservative Nmap service/version scan against
    an authorized target and return XML output.
    """

    with tempfile.NamedTemporaryFile(suffix=".xml") as temp:
        result = subprocess.run(
            [
                "nmap",
                "-sV",
                "-T3",
                "-oX",
                temp.name,
                target,
            ],
            capture_output=True,
            text=True,
            timeout=600,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Nmap failed: {result.stderr.strip()}"
            )

        temp.seek(0)
        return temp.read()
