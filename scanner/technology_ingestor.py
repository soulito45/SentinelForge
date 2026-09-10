from datetime import datetime

from sqlalchemy.orm import Session

from backend.app.models import Asset, Technology


def store_technologies(
    db: Session,
    asset: Asset,
    technologies: list[str],
) -> int:
    """
    Store the current technology state for an asset.

    Technologies are retained for historical tracking.

    Technologies observed in the current scan:
        status = active
        last_seen = current time

    Technologies not observed in the current scan:
        status = inactive

    Historical rows are never deleted.
    """

    now = datetime.utcnow()

    existing = {
        technology.name: technology
        for technology in asset.technologies
    }

    current_technologies = {
        name.strip()
        for name in technologies
        if name and name.strip()
    }

    stored_count = 0

    # ----------------------------------------------
    # Mark previously active technologies inactive
    # if they are absent from the current scan
    # ----------------------------------------------

    for technology in existing.values():
        if (
            technology.status == "active"
            and technology.name not in current_technologies
        ):
            technology.status = "inactive"

    # ----------------------------------------------
    # Store/update technologies observed now
    # ----------------------------------------------

    for name in current_technologies:

        if name in existing:
            technology = existing[name]

            technology.status = "active"
            technology.last_seen = now

        else:
            technology = Technology(
                asset_id=asset.id,
                name=name,
                status="active",
                first_seen=now,
                last_seen=now,
            )

            db.add(technology)
            stored_count += 1

    db.commit()

    return stored_count