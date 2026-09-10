from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base


class Technology(Base):
    __tablename__ = "technologies"

    id: Mapped[int] = mapped_column(primary_key=True)

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
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

    asset = relationship(
        "Asset",
        back_populates="technologies",
    )

    __table_args__ = (
        UniqueConstraint(
            "asset_id",
            "name",
            name="uq_asset_technology",
        ),
    )