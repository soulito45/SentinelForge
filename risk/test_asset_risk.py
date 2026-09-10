from backend.app.database import SessionLocal
from backend.app.models import Asset
from risk.asset_risk import calculate_asset_risk


db = SessionLocal()

try:
    asset = (
        db.query(Asset)
        .filter(
            Asset.hostname == "test.sentinelforge.local"
        )
        .first()
    )

    if asset is None:
        raise RuntimeError("Test asset not found")

    result = calculate_asset_risk(
        db=db,
        asset=asset,
    )

    print()
    print("========== ASSET RISK ==========")

    for key, value in result.items():
        print(f"{key}: {value}")

finally:
    db.close()