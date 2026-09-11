from sqlalchemy.orm import Session

from backend.app.models import Asset, Domain, Scan

from scanner.discovery_pipeline import run_discovery
from scanner.nmap_pipeline import run_nmap_pipeline
from scanner.httpx_pipeline import run_httpx_pipeline
from scanner.nuclei_pipeline import run_nuclei_pipeline

from risk.asset_change_detector import detect_asset_changes
from risk.change_detector import detect_changes
from risk.asset_risk import calculate_asset_risk


def run_full_scan(
    db: Session,
    domain: Domain,
    scan: Scan,
) -> dict:
    """
    Run the complete RYNEX scan pipeline.

    Domain
      -> Discovery
      -> Nmap
      -> HTTPX
      -> Nuclei
      -> Change Detection
      -> Risk Calculation
    """

    print()
    print("==========================================")
    print("       RYNEX FULL SCAN")
    print("==========================================")
    print(f"[+] Domain: {domain.name}")
    print(f"[+] Scan ID: {scan.id}")

    # --------------------------------------------------
    # 1. Capture previous asset state
    # --------------------------------------------------

    previous_assets = {
        asset.hostname
        for asset in (
            db.query(Asset)
            .filter(Asset.domain_id == domain.id)
            .all()
        )
        if asset.status == "active"
    }

    print()
    print(f"[+] Previous active assets: {len(previous_assets)}")

    # --------------------------------------------------
    # 2. Discovery
    # --------------------------------------------------

    asset_count = run_discovery(
        db=db,
        domain_id=domain.id,
        domain_name=domain.name,
    )

    db.flush()

    # --------------------------------------------------
    # 3. Capture current asset state
    # --------------------------------------------------

    current_assets = {
        asset.hostname
        for asset in (
            db.query(Asset)
            .filter(Asset.domain_id == domain.id)
            .all()
        )
        if asset.status == "active"
    }

    print()
    print(f"[+] Current active assets: {len(current_assets)}")

    # --------------------------------------------------
    # 4. Detect asset changes
    # --------------------------------------------------

    asset_changes = detect_asset_changes(
        db=db,
        domain_id=domain.id,
        scan_id=scan.id,
        previous_assets=previous_assets,
        current_assets=current_assets,
    )

    print(
        f"[+] Asset changes detected: "
        f"{asset_changes}"
    )

    # --------------------------------------------------
    # 5. Process active assets
    # --------------------------------------------------

    port_changes = 0
    technology_changes = 0
    finding_changes = 0
    risk_calculated = 0

    assets = (
        db.query(Asset)
        .filter(
            Asset.domain_id == domain.id,
            Asset.status == "active",
        )
        .all()
    )

    for asset in assets:

        print()
        print("------------------------------------------")
        print(f"[+] Processing asset: {asset.hostname}")
        print("------------------------------------------")

        # ----------------------------------------------
        # Capture previous state BEFORE scanners modify DB
        # ----------------------------------------------

        previous_ports = {
            (
                port.port_number,
                port.protocol,
            )
            for port in asset.ports
            if port.state == "open"
        }

        previous_technologies = {
            technology.name
            for technology in asset.technologies
            if technology.status == "active"
        }

        previous_findings = {
            finding.template_id
            for finding in asset.findings
            if finding.status == "open"
        }

        # ----------------------------------------------
        # Nmap
        # ----------------------------------------------

        try:
            run_nmap_pipeline(
                db=db,
                asset=asset,
            )

        except Exception as error:
            print(
                f"[!] Nmap failed for "
                f"{asset.hostname}: {error}"
            )

        db.flush()

        # ----------------------------------------------
        # HTTPX
        # ----------------------------------------------

        try:
            run_httpx_pipeline(
                db=db,
                asset=asset,
            )

        except Exception as error:
            print(
                f"[!] HTTPX failed for "
                f"{asset.hostname}: {error}"
            )

        db.flush()

        # ----------------------------------------------
        # Nuclei
        # ----------------------------------------------

        try:
            run_nuclei_pipeline(
                db=db,
                asset=asset,
                scan_id=scan.id,
            )

        except Exception as error:
            print(
                f"[!] Nuclei failed for "
                f"{asset.hostname}: {error}"
            )

        db.flush()

        # ----------------------------------------------
        # Capture current state AFTER scanners
        # ----------------------------------------------

        current_ports = {
            (
                port.port_number,
                port.protocol,
            )
            for port in asset.ports
            if port.state == "open"
        }
        current_technologies = {
            technology.name
            for technology in asset.technologies
            if technology.status == "active"
      }
        

        current_findings = {
            finding.template_id
            for finding in asset.findings
            if finding.status == "open"
        }

        # ----------------------------------------------
        # Detect changes
        # ----------------------------------------------

        change_result = detect_changes(
            db=db,
            asset=asset,
            scan_id=scan.id,
            previous_ports=previous_ports,
            current_ports=current_ports,
            previous_technologies=previous_technologies,
            current_technologies=current_technologies,
            previous_findings=previous_findings,
            current_findings=current_findings,
        )

        port_changes += change_result["port_changes"]

        technology_changes += (
            change_result["technology_changes"]
        )

        finding_changes += (
            change_result["finding_changes"]
        )

        # ----------------------------------------------
        # Calculate asset risk
        # ----------------------------------------------

        risk_result = calculate_asset_risk(
            db=db,
            asset=asset,
        )

        risk_calculated += 1

        print(
            f"[+] Risk: "
            f"{risk_result['risk_score']} "
            f"({risk_result['risk_level']})"
        )

    # --------------------------------------------------
    # 6. Final database commit
    # --------------------------------------------------

    db.commit()

    total_changes = (
        asset_changes
        + port_changes
        + technology_changes
        + finding_changes
    )

    print()
    print("==========================================")
    print("       RYNEX SCAN COMPLETE")
    print("==========================================")
    print(f"[+] Assets discovered: {asset_count}")
    print(f"[+] Asset changes: {asset_changes}")
    print(f"[+] Port changes: {port_changes}")
    print(
        f"[+] Technology changes: "
        f"{technology_changes}"
    )
    print(f"[+] Finding changes: {finding_changes}")
    print(f"[+] Total changes: {total_changes}")
    print(
        f"[+] Assets risk calculated: "
        f"{risk_calculated}"
    )

    return {
        "assets_discovered": asset_count,
        "asset_changes": asset_changes,
        "port_changes": port_changes,
        "technology_changes": technology_changes,
        "finding_changes": finding_changes,
        "total_changes": total_changes,
        "assets_risk_calculated": risk_calculated,
    }