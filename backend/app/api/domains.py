import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.models import Domain

router = APIRouter(prefix="/domains", tags=["Domains"])


def _get_allowed_domains() -> set[str]:
    raw_value = os.getenv("ALLOWED_DOMAINS", "sentinelforge.local")
    return {
        item.strip().lower()
        for item in raw_value.split(",")
        if item.strip()
    }


@router.post("/")
def create_domain(name: str, db: Session = Depends(get_db)):
    normalized_name = name.strip().lower()
    allowed_domains = _get_allowed_domains()

    if normalized_name not in allowed_domains:
        raise HTTPException(
            status_code=403,
            detail=(
                "Domain creation is restricted to allowlisted project domains. "
                "Update ALLOWED_DOMAINS in your environment to add another owned domain."
            ),
        )

    existing_domain = (
        db.query(Domain)
        .filter(Domain.name == normalized_name)
        .first()
    )

    if existing_domain:
        return {
            "id": existing_domain.id,
            "name": existing_domain.name,
            "created_at": existing_domain.created_at,
        }

    domain = Domain(name=normalized_name)

    db.add(domain)
    db.commit()
    db.refresh(domain)

    return {
        "id": domain.id,
        "name": domain.name,
        "created_at": domain.created_at,
    }


@router.get("/")
def list_domains(db: Session = Depends(get_db)):
    domains = db.query(Domain).all()

    return [
        {
            "id": domain.id,
            "name": domain.name,
            "created_at": domain.created_at,
        }
        for domain in domains
    ]
