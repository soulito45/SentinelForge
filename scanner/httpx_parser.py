import json


def parse_httpx_output(output: str) -> list[dict]:
    """
    Parse HTTPX JSONL output into structured HTTP exposure data.
    """

    results = []

    for line in output.splitlines():
        line = line.strip()

        if not line:
            continue

        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue

        technologies = data.get("tech") or []

        if isinstance(technologies, str):
            technologies = [technologies]

        results.append(
            {
                "url": data.get("url"),
                "status_code": data.get("status_code"),
                "title": data.get("title"),
                "webserver": data.get("webserver"),
                "technologies": technologies,
                "host": data.get("host"),
                "host_ip": data.get("host_ip"),
                "scheme": data.get("scheme"),
                "content_type": data.get("content_type"),
            }
        )

    return results
