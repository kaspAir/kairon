from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database import Base
from app.shared.model_mixins import GovernanceFieldsMixin


class ObservationRecord(GovernanceFieldsMixin, Base):
    __tablename__ = "observation_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    decision_id: Mapped[str] = mapped_column(String(36), ForeignKey("decisions.id"), nullable=False)
    expected_benefit: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    actual_benefit: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    expected_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    actual_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    expected_risks: Mapped[str | None] = mapped_column(Text)
    actual_risks: Mapped[str | None] = mapped_column(Text)
    comment: Mapped[str | None] = mapped_column(Text)
    observed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    decision = relationship("Decision", back_populates="observation_records")
