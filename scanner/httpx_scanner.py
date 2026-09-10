import subprocess


def run_httpx(target: str) -> str:
    """
    Run ProjectDiscovery HTTPX against an authorized HTTP/HTTPS target
    and return JSON output.
    """

    result = subprocess.run(
        [
            "httpx-toolkit",
            "-silent",
            "-json",
            "-status-code",
            "-title",
            "-server",
            "-tech-detect",
            "-u",
            target,
        ],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"HTTPX failed: {result.stderr.strip()}"
        )

    return result.stdout
