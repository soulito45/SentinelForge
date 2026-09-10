import json


def parse_nuclei_output(output: str) -> list[dict]:
    """
    Parse Nuclei JSONL output into structured findings.
    """

    findings = []

    for line in output.splitlines():
        line = line.strip()

        if not line:
            continue

        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue

        info = data.get("info") or {}

        finding = {
            "template_id": data.get("template-id"),
            "name": info.get("name"),
            "severity": info.get("severity"),
            "matched_at": data.get("matched-at"),
            "host": data.get("host"),
            "type": data.get("type"),
            "evidence": data.get("matcher-name"),
        }

        if finding["template_id"] and finding["name"]:
            findings.append(finding)

    return findings
