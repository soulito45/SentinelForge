from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.models import (
    Asset,
    Change,
    Finding,
    IPAddress,
    Port,
    Technology,
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/overview")
def get_overview(db: Session = Depends(get_db)):
    assets = db.query(Asset).all()
    findings = db.query(Finding).all()
    ports = db.query(Port).all()

    return {
        "total_assets": len(assets),
        "active_assets": sum(
            1 for asset in assets
            if asset.status == "active"
        ),
        "open_ports": sum(
            1 for port in ports
            if port.state == "open"
        ),
        "open_findings": sum(
            1 for finding in findings
            if finding.status == "open"
        ),
        "risk_distribution": {
            "critical": sum(
                1 for asset in assets
                if asset.risk_level == "CRITICAL"
            ),
            "high": sum(
                1 for asset in assets
                if asset.risk_level == "HIGH"
            ),
            "medium": sum(
                1 for asset in assets
                if asset.risk_level == "MEDIUM"
            ),
            "low": sum(
                1 for asset in assets
                if asset.risk_level == "LOW"
            ),
        },
    }


@router.get("/assets")
def get_assets(db: Session = Depends(get_db)):
    assets = (
        db.query(Asset)
        .order_by(Asset.risk_score.desc())
        .all()
    )

    return [
        {
            "id": asset.id,
            "hostname": asset.hostname,
            "asset_type": asset.asset_type,
            "status": asset.status,
            "http_url": asset.http_url,
            "http_status": asset.http_status,
            "http_title": asset.http_title,
            "web_server": asset.web_server,
            "risk_score": asset.risk_score,
            "risk_level": asset.risk_level,
            "first_seen": asset.first_seen,
            "last_seen": asset.last_seen,
        }
        for asset in assets
    ]


@router.get("/assets/{asset_id}")
def get_asset_detail(
    asset_id: int,
    db: Session = Depends(get_db),
):
    asset = (
        db.query(Asset)
        .filter(Asset.id == asset_id)
        .first()
    )

    if asset is None:
        raise HTTPException(
            status_code=404,
            detail="Asset not found",
        )

    ips = (
        db.query(IPAddress)
        .filter(IPAddress.asset_id == asset.id)
        .all()
    )

    ports = (
        db.query(Port)
        .filter(Port.asset_id == asset.id)
        .order_by(Port.port_number)
        .all()
    )

    technologies = (
        db.query(Technology)
        .filter(Technology.asset_id == asset.id)
        .all()
    )

    findings = (
        db.query(Finding)
        .filter(Finding.asset_id == asset.id)
        .all()
    )

    changes = (
        db.query(Change)
        .filter(Change.asset_id == asset.id)
        .order_by(Change.detected_at.desc())
        .all()
    )

    return {
        "id": asset.id,
        "hostname": asset.hostname,
        "asset_type": asset.asset_type,
        "status": asset.status,
        "http_url": asset.http_url,
        "http_status": asset.http_status,
        "http_title": asset.http_title,
        "web_server": asset.web_server,
        "risk_score": asset.risk_score,
        "risk_level": asset.risk_level,
        "first_seen": asset.first_seen,
        "last_seen": asset.last_seen,
        "ip_addresses": [
            {
                "id": ip.id,
                "ip": ip.ip,
                "first_seen": ip.first_seen,
                "last_seen": ip.last_seen,
            }
            for ip in ips
        ],
        "ports": [
            {
                "id": port.id,
                "port": port.port_number,
                "protocol": port.protocol,
                "state": port.state,
                "service": port.service_name,
                "product": port.product,
                "version": port.version,
            }
            for port in ports
        ],
        "technologies": [
            {
                "id": technology.id,
                "name": technology.name,
                "category": technology.category,
                "status": technology.status,
            }
            for technology in technologies
        ],
        "findings": [
            {
                "id": finding.id,
                "template_id": finding.template_id,
                "title": finding.title,
                "severity": finding.severity,
                "status": finding.status,
                "evidence": finding.evidence,
                "first_seen": finding.first_seen,
                "last_seen": finding.last_seen,
            }
            for finding in findings
        ],
        "changes": [
            {
                "id": change.id,
                "scan_id": change.scan_id,
                "change_type": change.change_type,
                "description": change.description,
                "previous_value": change.previous_value,
                "current_value": change.current_value,
                "detected_at": change.detected_at,
            }
            for change in changes
        ],
    }


@router.get("/findings")
def get_findings(db: Session = Depends(get_db)):
    findings = (
        db.query(Finding)
        .order_by(Finding.last_seen.desc())
        .all()
    )

    return [
        {
            "id": finding.id,
            "asset_id": finding.asset_id,
            "template_id": finding.template_id,
            "title": finding.title,
            "severity": finding.severity,
            "status": finding.status,
            "first_seen": finding.first_seen,
            "last_seen": finding.last_seen,
        }
        for finding in findings
    ]


@router.get("/changes")
def get_changes(db: Session = Depends(get_db)):
    changes = (
        db.query(Change)
        .order_by(Change.detected_at.desc())
        .all()
    )

    return [
        {
            "id": change.id,
            "asset_id": change.asset_id,
            "scan_id": change.scan_id,
            "change_type": change.change_type,
            "description": change.description,
            "previous_value": change.previous_value,
            "current_value": change.current_value,
            "detected_at": change.detected_at,
        }
        for change in changes
    ]
