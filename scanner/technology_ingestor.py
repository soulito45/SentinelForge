from datetime import datetime

from sqlalchemy.orm import Session

from backend.app.models import Asset, Technology


def store_technologies(
    db: Session,
    asset: Asset,
    technologies: list[str],
) -> int:
    """
    Store or update technologies discovered for an asset.
    """

    now = datetime.utcnow()

    existing = {
        technology.name: technology
        for technology in asset.technologies
    }

    stored_count = 0

    for name in technologies:
        name = name.strip()

        if not name:
            continue

        if name in existing:
            existing[name].last_seen = now
        else:
            technology = Technology(
                asset_id=asset.id,
                name=name,
                first_seen=now,
                last_seen=now,
            )

            db.add(technology)
            stored_count += 1

    db.commit()

    return stored_count
