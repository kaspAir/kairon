from uuid import uuid4

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database import Base
from app.shared.model_mixins import GovernanceFieldsMixin


class Scenario(GovernanceFieldsMixin, Base):
    __tablename__ = "scenarios"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    decision_id: Mapped[str] = mapped_column(String(36), ForeignKey("decisions.id"), nullable=False)
    variant_id: Mapped[str] = mapped_column(String(36), ForeignKey("decision_variants.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    case_volume: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    processing_minutes_per_case: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    hourly_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)

    decision = relationship("Decision", back_populates="scenarios")
    variant = relationship("DecisionVariant", back_populates="scenarios")
    simulation_runs = relationship("SimulationRun", back_populates="scenario", cascade="all, delete-orphan")
    context_objects = relationship("DecisionContextObject", back_populates="scenario", cascade="all, delete-orphan")
