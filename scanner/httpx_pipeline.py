from sqlalchemy.orm import Session

from backend.app.models import Asset
from scanner.httpx_scanner import run_httpx
from scanner.httpx_parser import parse_httpx_output
from scanner.technology_ingestor import store_technologies


def run_httpx_pipeline(
    db: Session,
    asset: Asset,
) -> int:
    """
    Run HTTPX against web ports discovered by Nmap,
    parse HTTP metadata, and store technologies.
    """

    web_ports = {
        port.port_number
        for port in asset.ports
        if port.state == "open"
        and port.port_number in {80, 443, 8000, 8080, 8443}
    }

    if not web_ports:
        print(f"[!] No web ports found for {asset.hostname}")
        return 0

    port = next(
        (
            p
            for p in [80, 8000, 8080, 443, 8443]
            if p in web_ports
        ),
        None,
    )

    if port is None:
        print(f"[!] No usable web port found for {asset.hostname}")
        return 0

    scheme = "https" if port in {443, 8443} else "http"

    target = f"{scheme}://{asset.hostname}:{port}"

    print(f"[+] Asset: {asset.hostname}")
    print(f"[+] HTTPX target: {target}")

    output = run_httpx(target)

    results = parse_httpx_output(output)

    if not results:
        print("[!] HTTPX returned no results")
        return 0

    result = results[0]

    asset.http_url = result.get("url")
    asset.http_status = result.get("status_code")
    asset.http_title = result.get("title")
    asset.web_server = result.get("webserver")

    technologies = result.get("technologies") or []

    count = store_technologies(
        db=db,
        asset=asset,
        technologies=technologies,
    )

    db.commit()

    print(f"[+] HTTP status: {asset.http_status}")
    print(f"[+] Title: {asset.http_title}")
    print(f"[+] Web server: {asset.web_server}")
    print(f"[+] Technologies: {technologies}")
    print(f"[+] New technologies stored: {count}")

    return count