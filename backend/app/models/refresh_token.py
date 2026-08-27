import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    String,
    DateTime,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class RefreshToken(Base):

    __tablename__ = "refresh_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    token_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        index=True
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    replaced_by: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            "refresh_tokens.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )