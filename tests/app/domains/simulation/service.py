from app.domains.assessment.models import ImpactAssessment, SimulationRun
from app.domains.scenario.models import Scenario
from app.shared.errors import NotFoundError


class SimulationService:
    def __init__(self, session):
        self.session = session

    def run_deterministic_simulation(self, scenario_id: str, created_by: str = "system") -> SimulationRun:
        scenario = self.session.get(Scenario, scenario_id)
        if scenario is None:
            raise NotFoundError("Scenario not found")

        total_processing_hours = float(scenario.case_volume) * float(scenario.processing_minutes_per_case) / 60
        total_cost = total_processing_hours * float(scenario.hourly_cost)
        run = SimulationRun(
            scenario_id=scenario_id,
            total_processing_hours=round(total_processing_hours, 2),
            total_cost=round(total_cost, 2),
            deterministic_formula="case_volume * processing_minutes_per_case / 60 * hourly_cost",
            created_by=created_by,
        )
        self.session.add(run)
        self.session.flush()

        expected_benefit = float(scenario.variant.expected_benefit)
        estimated_cost = float(scenario.variant.estimated_cost)
        impact = ImpactAssessment(
            simulation_run_id=run.id,
            cost_impact=round(total_cost + estimated_cost, 2),
            benefit_impact=round(expected_benefit, 2),
            net_impact=round(expected_benefit - total_cost - estimated_cost, 2),
            confidence_score=0.70,
            created_by=created_by,
        )
        self.session.add(impact)
        self.session.flush()
        return run
