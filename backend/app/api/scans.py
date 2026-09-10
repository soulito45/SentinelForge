from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.models import Domain, Scan
from scanner.scan_pipeline import run_full_scan


router = APIRouter(prefix="/scans", tags=["Scans"])


@router.post("/")
def start_scan(
    domain_id: int,
    db: Session = Depends(get_db),
):
    domain = (
        db.query(Domain)
        .filter(Domain.id == domain_id)
        .first()
    )

    if domain is None:
        raise HTTPException(
            status_code=404,
            detail="Domain not found",
        )

    scan = Scan(
        domain_id=domain.id,
        status="running",
        started_at=datetime.utcnow(),
    )

    db.add(scan)
    db.commit()
    db.refresh(scan)

    try:
        result = run_full_scan(
            db=db,
            domain=domain,
            scan=scan,
        )

        scan.status = "completed"
        scan.completed_at = datetime.utcnow()

        db.commit()
        db.refresh(scan)

        return {
            "scan_id": scan.id,
            "status": scan.status,
            "domain": domain.name,
            "assets_discovered": result["assets_discovered"],
            "asset_changes": result["asset_changes"],
            "port_changes": result["port_changes"],
            "technology_changes": result["technology_changes"],
            "finding_changes": result["finding_changes"],
            "total_changes": result["total_changes"],
            "assets_risk_calculated": (
                result["assets_risk_calculated"]
            ),
            "started_at": scan.started_at,
            "completed_at": scan.completed_at,
        }

    except Exception as error:
        scan.status = "failed"
        scan.completed_at = datetime.utcnow()

        db.commit()

        raise HTTPException(
            status_code=500,
            detail=f"Scan failed: {str(error)}",
        )


@router.get("/{scan_id}")
def get_scan(
    scan_id: int,
    db: Session = Depends(get_db),
):
    scan = (
        db.query(Scan)
        .filter(Scan.id == scan_id)
        .first()
    )

    if scan is None:
        raise HTTPException(
            status_code=404,
            detail="Scan not found",
        )

    return {
        "scan_id": scan.id,
        "domain_id": scan.domain_id,
        "status": scan.status,
        "started_at": scan.started_at,
        "completed_at": scan.completed_at,
    }