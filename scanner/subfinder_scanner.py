import subprocess


def parse_subfinder_output(output: str) -> list[str]:
    """
    Parse Subfinder output, normalize hostnames,
    remove duplicates, and return sorted results.
    """

    subdomains = {
        line.strip().lower().rstrip(".")
        for line in output.splitlines()
        if line.strip()
    }

    return sorted(subdomains)


def discover_subdomains(domain: str) -> list[str]:
    """
    Run Subfinder against an authorized domain.
    """

    result = subprocess.run(
        [
            "subfinder",
            "-d",
            domain,
            "-silent",
        ],
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Subfinder failed: {result.stderr.strip()}"
        )

    return parse_subfinder_output(result.stdout)
