from uuid import uuid4

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database import Base
from app.shared.model_mixins import GovernanceFieldsMixin


class Decision(GovernanceFieldsMixin, Base):
    __tablename__ = "decisions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    context: Mapped[str | None] = mapped_column(Text)

    variants = relationship("DecisionVariant", back_populates="decision", cascade="all, delete-orphan")
    scenarios = relationship("Scenario", back_populates="decision", cascade="all, delete-orphan")
    risk_assessments = relationship("RiskAssessment", back_populates="decision", cascade="all, delete-orphan")
    approval_records = relationship("ApprovalRecord", back_populates="decision", cascade="all, delete-orphan")
    decision_records = relationship("DecisionRecord", back_populates="decision", cascade="all, delete-orphan")
    observation_records = relationship("ObservationRecord", back_populates="decision", cascade="all, delete-orphan")


class DecisionVariant(GovernanceFieldsMixin, Base):
    __tablename__ = "decision_variants"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    decision_id: Mapped[str] = mapped_column(String(36), ForeignKey("decisions.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    estimated_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    expected_benefit: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)

    decision = relationship("Decision", back_populates="variants")
    scenarios = relationship("Scenario", back_populates="variant", cascade="all, delete-orphan")
