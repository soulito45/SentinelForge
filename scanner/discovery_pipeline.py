from sqlalchemy.orm import Session

from scanner.subfinder_scanner import discover_subdomains
from scanner.dns_resolver import resolve_hostname
from scanner.asset_ingestor import store_asset


def run_discovery(
    db: Session,
    domain_id: int,
    domain_name: str,
) -> int:
    """
    Run the complete discovery pipeline:

    Domain
      -> Subfinder
      -> Normalize/Deduplicate
      -> DNS Resolution
      -> PostgreSQL
    """

    print(f"[+] Starting discovery for {domain_name}")

    # 1. Discover subdomains
    subdomains = discover_subdomains(domain_name)

    print(f"[+] Discovered {len(subdomains)} unique hostnames")

    asset_count = 0

    # 2. Resolve and store each hostname
    for hostname in subdomains:
        ips = resolve_hostname(hostname)

        print(f"[+] {hostname} -> {ips}")

        store_asset(
            db=db,
            domain_id=domain_id,
            hostname=hostname,
            ips=ips,
        )

        asset_count += 1

    # 3. Commit everything
    db.commit()

    print(f"[+] Discovery completed: {asset_count} assets processed")

    return asset_count
