import subprocess


def run_nuclei(target: str) -> str:
    """
    Run a controlled Nuclei scan against an authorized target
    and return JSONL output.
    """

    result = subprocess.run(
        [
            "nuclei",
            "-u",
            target,
            "-t",
            "http/exposures/apis/swagger-api.yaml",
            "-jsonl",
            "-silent",
            "-rate-limit",
            "10",
        ],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Nuclei failed: {result.stderr.strip()}"
        )

    return result.stdout