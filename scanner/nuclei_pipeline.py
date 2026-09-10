from sqlalchemy.orm import Session

from backend.app.models import Asset
from scanner.nuclei_scanner import run_nuclei
from scanner.nuclei_parser import parse_nuclei_output
from scanner.finding_ingestor import store_findings


def run_nuclei_pipeline(
    db: Session,
    asset: Asset,
    scan_id: int,
) -> int:
    """
    Run Nuclei against an HTTP-enabled asset,
    parse findings, and store/update their lifecycle.
    """

    if not asset.http_url:
        print(f"[!] No HTTP URL found for {asset.hostname}")
        return 0

    target = asset.http_url

    print(f"[+] Nuclei target: {target}")

    output = run_nuclei(target)

    findings = parse_nuclei_output(output)

    print(f"[+] Parsed {len(findings)} findings")

    count = store_findings(
        db=db,
        asset=asset,
        scan_id=scan_id,
        findings=findings,
    )

    print(f"[+] New findings stored: {count}")

    return count