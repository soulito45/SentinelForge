from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base


class IPAddress(Base):
    __tablename__ = "ip_addresses"

    id: Mapped[int] = mapped_column(primary_key=True)

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id"),
        nullable=False,
        index=True,
    )

    ip: Mapped[str] = mapped_column(
        String(45),
        nullable=False,
        index=True,
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

    asset = relationship(
        "Asset",
        back_populates="ip_addresses",
    )

    __table_args__ = (
        UniqueConstraint(
            "asset_id",
            "ip",
            name="uq_asset_ip",
        ),
    )
