from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
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

    domain = relationship(
        "Domain",
        back_populates="assets",
    )

    ip_addresses = relationship(
        "IPAddress",
        back_populates="asset",
        cascade="all, delete-orphan",
    )
