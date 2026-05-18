from __future__ import annotations

from datetime import datetime

from app.domains.assessment.models import RiskAssessment
from app.domains.context.models import DecisionContextObject
from app.domains.decision.models import Decision, DecisionVariant
from app.domains.governance.models import ApprovalRecord
from app.domains.governance.service import GovernanceService
from app.domains.observation.service import ObservationService
from app.domains.scenario.models import Scenario
from app.domains.simulation.service import SimulationService

DEMO_DECISION_TITLE = "AI-based Invoice Processing Automation"
DEMO_CREATED_BY = "kairon-demo-seed"


def seed_golden_demo(session) -> Decision:
    """Create an idempotent Enterprise demo case for the KAIRON MVP.

    The seed intentionally uses existing domain models and services. It does not
    introduce new business logic; it creates realistic data so the workspace can
    demonstrate the full decision-intelligence flow end to end.
    """
    existing = session.query(Decision).filter(Decision.title == DEMO_DECISION_TITLE).one_or_none()
    if existing is not None:
        return existing

    decision = Decision(
        title=DEMO_DECISION_TITLE,
        context=(
            "Enterprise finance is evaluating whether AI-assisted invoice processing can reduce manual effort, "
            "cycle time and exception handling costs while keeping governance and human accountability intact."
        ),
        status="in_review",
        created_by=DEMO_CREATED_BY,
    )
    session.add(decision)
    session.flush()

    variants = [
        DecisionVariant(
            decision_id=decision.id,
            name="A · Keep manual processing",
            description="Baseline: continue current manual validation, routing and exception handling.",
            estimated_cost=0,
            expected_benefit=0,
            status="draft",
            created_by=DEMO_CREATED_BY,
        ),
        DecisionVariant(
            decision_id=decision.id,
            name="B · AI-assisted triage",
            description="AI extracts invoice data and proposes routing; finance specialists remain in the approval loop.",
            estimated_cost=120000,
            expected_benefit=360000,
            status="simulated",
            created_by=DEMO_CREATED_BY,
        ),
        DecisionVariant(
            decision_id=decision.id,
            name="C · AI automation with governance gate",
            description="Higher automation rate with explicit human review for exceptions, high-value invoices and uncertain predictions.",
            estimated_cost=260000,
            expected_benefit=520000,
            status="risk_reviewed",
            created_by=DEMO_CREATED_BY,
        ),
    ]
    session.add_all(variants)
    session.flush()

    scenarios = [
        Scenario(
            decision_id=decision.id,
            variant_id=variants[0].id,
            name="Current annual invoice volume",
            description="48,000 invoices per year, largely manual processing and validation.",
            case_volume=48000,
            processing_minutes_per_case=12,
            hourly_cost=75,
            status="draft",
            created_by=DEMO_CREATED_BY,
        ),
        Scenario(
            decision_id=decision.id,
            variant_id=variants[1].id,
            name="30% automation with finance review",
            description="AI-assisted extraction and routing; finance keeps control over payment release.",
            case_volume=48000,
            processing_minutes_per_case=6.5,
            hourly_cost=75,
            status="simulated",
            created_by=DEMO_CREATED_BY,
        ),
        Scenario(
            decision_id=decision.id,
            variant_id=variants[2].id,
            name="65% automation with exception governance",
            description="Automation for standard invoices; explicit governance gate for exceptions and high-value cases.",
            case_volume=48000,
            processing_minutes_per_case=3.8,
            hourly_cost=75,
            status="simulated",
            created_by=DEMO_CREATED_BY,
        ),
    ]
    session.add_all(scenarios)
    session.flush()

    confidence_by_scenario = {
        scenarios[0].id: 0.82,
        scenarios[1].id: 0.76,
        scenarios[2].id: 0.84,
    }
    for scenario in scenarios:
        run = SimulationService(session).run_deterministic_simulation(scenario.id, created_by=DEMO_CREATED_BY)
        run.status = "simulated"
        if run.impact_assessment:
            run.impact_assessment.confidence_score = confidence_by_scenario[scenario.id]
            run.impact_assessment.status = "simulated"

    risks = [
        RiskAssessment(
            decision_id=decision.id,
            summary="Invoice data quality varies across suppliers and regions.",
            severity="medium",
            mitigation="Start with top suppliers, measure exception rate, and keep manual fallback paths.",
            status="risk_reviewed",
            created_by=DEMO_CREATED_BY,
        ),
        RiskAssessment(
            decision_id=decision.id,
            summary="High-value or unusual invoices may require stricter human review.",
            severity="high",
            mitigation="Route uncertain, high-value and policy-sensitive cases through a governance gate.",
            status="risk_reviewed",
            created_by=DEMO_CREATED_BY,
        ),
        RiskAssessment(
            decision_id=decision.id,
            summary="Supplier onboarding and change management may reduce short-term adoption speed.",
            severity="medium",
            mitigation="Pilot with one business unit and publish clear exception-handling guidance.",
            status="risk_reviewed",
            created_by=DEMO_CREATED_BY,
        ),
    ]
    session.add_all(risks)

    context_objects = [
        DecisionContextObject(
            decision_id=decision.id,
            context_type="process",
            name="Current invoice intake and approval process",
            description="Invoices are received through email and supplier portals, validated manually and routed to finance approvers.",
            source="Finance operations workshop",
            owner="Finance Process Owner",
            confidence="high",
        ),
        DecisionContextObject(
            decision_id=decision.id,
            scenario_id=scenarios[1].id,
            context_type="workforce",
            name="Accounts payable specialist capacity",
            description="Manual validation currently consumes roughly 4.2 FTE across standard and exception handling work.",
            source="Capacity estimate based on 48,000 invoices/year",
            owner="AP Operations Lead",
            confidence="medium",
        ),
        DecisionContextObject(
            decision_id=decision.id,
            context_type="organization",
            name="Finance governance gate",
            description="High-value invoices and low-confidence AI suggestions remain under explicit human approval.",
            source="Architecture Board decision",
            owner="Architecture Board",
            confidence="high",
        ),
        DecisionContextObject(
            decision_id=decision.id,
            context_type="constraint",
            name="No autonomous payment release",
            description="AI may recommend routing and extraction results, but payment release remains a human decision.",
            source="AI governance principle",
            owner="Governance Lead",
            confidence="high",
        ),
        DecisionContextObject(
            decision_id=decision.id,
            context_type="assumption",
            name="Supplier invoice format stability",
            description="Automation benefit assumes the top suppliers keep invoice formats stable during the pilot.",
            source="Pilot assumption",
            owner="Finance Process Owner",
            confidence="medium",
        ),
        DecisionContextObject(
            decision_id=decision.id,
            context_type="metric",
            name="Cycle time and exception rate",
            description="Primary KPI focus: reduce processing cycle time while keeping exception rate transparent.",
            source="MVP KPI definition",
            owner="Decision Owner",
            confidence="medium",
        ),
        DecisionContextObject(
            decision_id=decision.id,
            context_type="risk",
            name="Supplier data quality risk",
            description="Supplier invoice formats vary by region and can reduce AI extraction reliability during rollout.",
            source="Finance pilot risk review",
            owner="AP Operations Lead",
            confidence="high",
            metadata_json={
                "category": "data_quality",
                "probability": "high",
                "impact": "high",
                "severity": "critical",
                "impact_area": "operations",
                "mitigation": "Start with top suppliers, monitor exception rate weekly and keep manual fallback paths.",
                "risk_owner": "AP Operations Lead",
                "review_required": True,
            },
        ),
        DecisionContextObject(
            decision_id=decision.id,
            context_type="risk",
            name="Human approval bypass risk",
            description="Automation pressure may lead teams to treat AI suggestions as decisions instead of advisory inputs.",
            source="AI governance review",
            owner="Governance Lead",
            confidence="medium",
            metadata_json={
                "category": "governance",
                "probability": "medium",
                "impact": "high",
                "severity": "high",
                "impact_area": "compliance",
                "mitigation": "Route high-value, low-confidence and policy-sensitive invoices through mandatory human review.",
                "risk_owner": "Governance Lead",
                "review_required": True,
            },
        ),
    ]
    session.add_all(context_objects)
    session.flush()

    approvals = [
        ApprovalRecord(
            decision_id=decision.id,
            approved_by="Finance Process Owner",
            comment="Business case is plausible if exception governance remains explicit.",
            status="approved",
            created_by=DEMO_CREATED_BY,
        ),
        ApprovalRecord(
            decision_id=decision.id,
            approved_by="Architecture Board",
            comment="Approved for controlled pilot; no autonomous payment decisions by AI.",
            status="approved",
            created_by=DEMO_CREATED_BY,
        ),
    ]
    session.add_all(approvals)
    session.flush()

    ObservationService(session).create_observation_record(
        decision_id=decision.id,
        expected_benefit=360000,
        actual_benefit=315000,
        expected_cost=120000,
        actual_cost=145000,
        expected_risks="Data quality and exception handling risk expected during pilot.",
        actual_risks="Exception handling risk higher than expected for suppliers with inconsistent invoice formats.",
        comment="Pilot shows clear benefit, but reassessment is needed before broader rollout.",
        observed_at=datetime(2026, 5, 1, 9, 30),
        created_by=DEMO_CREATED_BY,
    )

    GovernanceService(session).create_decision_record(decision.id, created_by=DEMO_CREATED_BY)
    decision.status = "reassessment_needed"
    session.flush()
    return decision
