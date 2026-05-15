from uuid import uuid4

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database import Base
from app.shared.model_mixins import GovernanceFieldsMixin


class ApprovalRecord(GovernanceFieldsMixin, Base):
    __tablename__ = "approval_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    decision_id: Mapped[str] = mapped_column(String(36), ForeignKey("decisions.id"), nullable=False)
    approved_by: Mapped[str] = mapped_column(String(120), nullable=False)
    comment: Mapped[str | None] = mapped_column(Text)

    decision = relationship("Decision", back_populates="approval_records")


class DecisionRecord(GovernanceFieldsMixin, Base):
    __tablename__ = "decision_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    decision_id: Mapped[str] = mapped_column(String(36), ForeignKey("decisions.id"), nullable=False)
    record_text: Mapped[str] = mapped_column(Text, nullable=False)

    decision = relationship("Decision", back_populates="decision_records")
