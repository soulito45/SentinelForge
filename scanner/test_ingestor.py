from backend.app.database import SessionLocal
from backend.app.models import Domain
from scanner.asset_ingestor import store_asset


db = SessionLocal()

try:
    domain = db.query(Domain).first()

    if domain is None:
        raise RuntimeError("No domain exists in the database.")

    asset = store_asset(
        db=db,
        domain_id=domain.id,
        hostname="api.example.com",
        ips=["93.184.216.34"],
    )

    db.commit()

    print("Asset stored successfully")
    print("Asset ID:", asset.id)
    print("Hostname:", asset.hostname)

    for ip in asset.ip_addresses:
        print("IP:", ip.ip)

finally:
    db.close()
