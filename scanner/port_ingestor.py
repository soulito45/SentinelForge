from datetime import datetime

from sqlalchemy.orm import Session

from backend.app.models import Asset, Port


def store_ports(
    db: Session,
    asset: Asset,
    ports: list[dict],
) -> int:
    """
    Store or update Nmap port results for an asset.
    """

    now = datetime.utcnow()
    stored_count = 0

    for result in ports:
        port_number = result["port"]
        protocol = result["protocol"]

        existing_port = (
            db.query(Port)
            .filter(
                Port.asset_id == asset.id,
                Port.port_number == port_number,
                Port.protocol == protocol,
            )
            .first()
        )

        if existing_port is None:
            port_record = Port(
                asset_id=asset.id,
                port_number=port_number,
                protocol=protocol,
                state=result.get("state") or "unknown",
                service_name=result.get("service_name"),
                product=result.get("product"),
                version=result.get("version"),
                first_seen=now,
                last_seen=now,
            )

            db.add(port_record)
            stored_count += 1

        else:
            existing_port.state = result.get("state") or "unknown"
            existing_port.service_name = result.get("service_name")
            existing_port.product = result.get("product")
            existing_port.version = result.get("version")
            existing_port.last_seen = now

    db.commit()

    return stored_count
