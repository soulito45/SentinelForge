from datetime import datetime

from sqlalchemy.orm import Session

from backend.app.models import Asset, IPAddress


def store_asset(
    db: Session,
    domain_id: int,
    hostname: str,
    ips: list[str],
) -> Asset:
    """
    Create or update an asset and its resolved IP addresses.
    """

    hostname = hostname.lower().rstrip(".")

    asset = (
        db.query(Asset)
        .filter(Asset.hostname == hostname)
        .first()
    )

    now = datetime.utcnow()

    if asset is None:
        asset = Asset(
            domain_id=domain_id,
            hostname=hostname,
            asset_type="subdomain",
            status="active",
            first_seen=now,
            last_seen=now,
        )

        db.add(asset)
        db.flush()

    else:
        asset.last_seen = now
        asset.status = "active"

    existing_ips = {
        ip_record.ip
        for ip_record in asset.ip_addresses
    }

    for ip in ips:
        if ip not in existing_ips:
            asset.ip_addresses.append(
                IPAddress(
                    ip=ip,
                    first_seen=now,
                    last_seen=now,
                )
            )
        else:
            for ip_record in asset.ip_addresses:
                if ip_record.ip == ip:
                    ip_record.last_seen = now

    return asset
