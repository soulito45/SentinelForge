from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True)

    domain_id: Mapped[int] = mapped_column(
        ForeignKey("domains.id"),
        nullable=False,
        index=True,
    )

    hostname: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    asset_type: Mapped[str] = mapped_column(
        String(50),
        default="subdomain",
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="active",
        nullable=False,
    )

    first_seen: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    last_seen: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    http_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    http_status: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    http_title: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    web_server: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    risk_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    risk_level: Mapped[str] = mapped_column(
        String(20),
        default="LOW",
        nullable=False,
    )

    risk_updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    domain = relationship(
        "Domain",
        back_populates="assets",
    )

    ip_addresses = relationship(
        "IPAddress",
        back_populates="asset",
        cascade="all, delete-orphan",
    )

    ports = relationship(
        "Port",
        back_populates="asset",
        cascade="all, delete-orphan",
    )

    technologies = relationship(
        "Technology",
        back_populates="asset",
        cascade="all, delete-orphan",
    )

    findings = relationship(
        "Finding",
        back_populates="asset",
        cascade="all, delete-orphan",
    )