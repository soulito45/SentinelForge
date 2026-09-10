from datetime import datetime

from sqlalchemy.orm import Session

from backend.app.models import Asset, Port


def store_ports(
    db: Session,
    asset: Asset,
    ports: list[dict],
) -> int:
    """
    Store the current Nmap port state for an asset.

    Existing ports that are not present in the current scan
    are marked closed instead of being deleted, preserving history.
    """

    now = datetime.utcnow()
    stored_count = 0

    current_ports = {
        (
            result["port"],
            result["protocol"],
        )
        for result in ports
    }

    existing_ports = {
        (
            port.port_number,
            port.protocol,
        ): port
        for port in asset.ports
    }

    # ----------------------------------------------
    # Store/update ports found in current scan
    # ----------------------------------------------

    for result in ports:
        port_number = result["port"]
        protocol = result["protocol"]

        key = (port_number, protocol)

        if key in existing_ports:
            port_record = existing_ports[key]

            port_record.state = result.get("state") or "unknown"
            port_record.service_name = result.get("service_name")
            port_record.product = result.get("product")
            port_record.version = result.get("version")
            port_record.last_seen = now

        else:
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

    # ----------------------------------------------
    # Mark previously open ports as closed
    # if they were not observed in this scan
    # ----------------------------------------------

    for key, port_record in existing_ports.items():

        if (
            port_record.state == "open"
            and key not in current_ports
        ):
            port_record.state = "closed"

    db.commit()

    return stored_count