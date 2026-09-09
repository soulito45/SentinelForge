from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.models import Domain

router = APIRouter(prefix="/domains", tags=["Domains"])


@router.post("/")
def create_domain(name: str, db: Session = Depends(get_db)):
    domain = Domain(name=name)

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
