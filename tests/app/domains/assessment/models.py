from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database import Base
from app.shared.model_mixins import GovernanceFieldsMixin


class SimulationRun(GovernanceFieldsMixin, Base):
    __tablename__ = "simulation_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    scenario_id: Mapped[str] = mapped_column(String(36), ForeignKey("scenarios.id"), nullable=False)
    total_processing_hours: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    total_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    deterministic_formula: Mapped[str] = mapped_column(String(300), nullable=False)
    simulated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    scenario = relationship("Scenario", back_populates="simulation_runs")
    impact_assessment = relationship("ImpactAssessment", back_populates="simulation_run", uselist=False, cascade="all, delete-orphan")


class ImpactAssessment(GovernanceFieldsMixin, Base):
    __tablename__ = "impact_assessments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    simulation_run_id: Mapped[str] = mapped_column(String(36), ForeignKey("simulation_runs.id"), nullable=False)
    cost_impact: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    benefit_impact: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    net_impact: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False, default=0.70)

    simulation_run = relationship("SimulationRun", back_populates="impact_assessment")


class RiskAssessment(GovernanceFieldsMixin, Base):
    __tablename__ = "risk_assessments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    decision_id: Mapped[str] = mapped_column(String(36), ForeignKey("decisions.id"), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")
    mitigation: Mapped[str | None] = mapped_column(Text)

    decision = relationship("Decision", back_populates="risk_assessments")
