from sqlalchemy.orm import Session

from backend.app.models import Asset
from risk.change_detector import record_change


def detect_asset_changes(
    db: Session,
    domain_id: int,
    scan_id: int,
    previous_assets: set[str],
    current_assets: set[str],
) -> int:
    """
    Detect newly discovered and previously observed assets
    that are no longer present.
    """

    changes = 0

    new_assets = current_assets - previous_assets
    removed_assets = previous_assets - current_assets

    for hostname in sorted(new_assets):
        asset = (
            db.query(Asset)
            .filter(
                Asset.domain_id == domain_id,
                Asset.hostname == hostname,
            )
            .first()
        )

        if asset is None:
            continue

        record_change(
            db=db,
            asset=asset,
            scan_id=scan_id,
            change_type="NEW_ASSET",
            description=f"New asset discovered: {hostname}",
            previous_value=None,
            current_value=hostname,
        )

        changes += 1

    for hostname in sorted(removed_assets):
        asset = (
            db.query(Asset)
            .filter(
                Asset.domain_id == domain_id,
                Asset.hostname == hostname,
            )
            .first()
        )

        if asset is None:
            continue

        asset.status = "inactive"

        record_change(
            db=db,
            asset=asset,
            scan_id=scan_id,
            change_type="REMOVED_ASSET",
            description=f"Asset no longer discovered: {hostname}",
            previous_value=hostname,
            current_value=None,
        )

        changes += 1

    db.commit()

    return changes
