from backend.app.database import SessionLocal
from backend.app.models import Asset, Port
from scanner.port_ingestor import store_ports


db = SessionLocal()

try:
    asset = db.query(Asset).first()

    if asset is None:
        print("No asset exists in the database.")
        print("Create an authorized test asset before running this test.")
        raise SystemExit(1)

    sample_ports = [
        {
            "ip": "192.168.1.10",
            "port": 22,
            "protocol": "tcp",
            "state": "open",
            "service_name": "ssh",
            "product": "OpenSSH",
            "version": "9.6",
        },
        {
            "ip": "192.168.1.10",
            "port": 443,
            "protocol": "tcp",
            "state": "open",
            "service_name": "https",
            "product": "nginx",
            "version": "1.24.0",
        },
    ]

    count = store_ports(
        db=db,
        asset=asset,
        ports=sample_ports,
    )

    print(f"New ports stored: {count}")

    saved_ports = (
        db.query(Port)
        .filter(Port.asset_id == asset.id)
        .all()
    )

    for port in saved_ports:
        print(
            f"{port.port_number}/{port.protocol} "
            f"{port.state} "
            f"{port.service_name} "
            f"{port.product} "
            f"{port.version}"
        )

finally:
    db.close()
