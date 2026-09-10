from sqlalchemy.orm import Session

from backend.app.models import Asset
from scanner.nmap_scanner import run_nmap
from scanner.nmap_parser import parse_nmap_xml
from scanner.port_ingestor import store_ports


def run_nmap_pipeline(
    db: Session,
    asset: Asset,
) -> int:
    """
    Run Nmap against the asset's resolved IP address,
    parse the XML output, and store discovered ports.
    """

    if not asset.ip_addresses:
        raise RuntimeError(
            f"No resolved IP address found for {asset.hostname}"
        )

    target_ip = asset.ip_addresses[0].ip

    print(f"[+] Asset: {asset.hostname}")
    print(f"[+] Scanning IP: {target_ip}")

    xml_output = run_nmap(target_ip)

    results = parse_nmap_xml(xml_output)

    print(f"[+] Parsed {len(results)} ports")

    count = store_ports(
        db=db,
        asset=asset,
        ports=results,
    )

    print(f"[+] Stored {count} new ports")

    return count
