"""
Operational Risk Assessment Engine.

Evaluates known risk factors strictly from provided and verifiable inputs.
Does not invent categories or infer unavailable data like weather/congestion.
"""

from dataclasses import dataclass, field
from app.optimization.risk_engine.schemas import RiskStatus
from app.optimization.vessel_feasibility.evaluator import FeasibilityReport, FeasibilityStatus


@dataclass
class RiskFinding:
    factor: str
    status: RiskStatus
    finding: str
    missing_info: str = ""


@dataclass
class RiskAssessmentReport:
    findings: list[RiskFinding] = field(default_factory=list)


def assess_operational_risks(
    feasibility_report: FeasibilityReport,
    schedule_feasible: bool = False,
    schedule_evaluated: bool = False,
    cost_is_complete: bool = False,
) -> RiskAssessmentReport:
    findings = []

    # 1. Vessel and Port Feasibility Risk
    if feasibility_report.summary.startswith("NOT_CONFIGURED"):
        findings.append(RiskFinding(
            factor="Vessel/Port Compatibility",
            status=RiskStatus.INSUFFICIENT_DATA,
            finding="Cannot verify if vessels fit port dimensions.",
            missing_info="Vessel master and port berth master reference data."
        ))
    else:
        infeasible_count = sum(1 for v in feasibility_report.vessel_class_results if v.overall_status == FeasibilityStatus.INFEASIBLE)
        insufficient_count = sum(1 for v in feasibility_report.vessel_class_results if v.overall_status == FeasibilityStatus.INSUFFICIENT_DATA)
        feasible_count = sum(1 for v in feasibility_report.vessel_class_results if v.overall_status == FeasibilityStatus.FEASIBLE)
        
        if feasible_count == 0:
            finding_text = "High Risk: No feasible vessel types identified for this route/cargo."
        else:
            finding_text = f"Low/Moderate Risk: {feasible_count} feasible vessel types found. ({infeasible_count} infeasible, {insufficient_count} unverified)."
            
        findings.append(RiskFinding(
            factor="Vessel/Port Compatibility",
            status=RiskStatus.EVALUATED,
            finding=finding_text
        ))

    # 2. Schedule and Deadline Risk
    if schedule_evaluated:
        if not schedule_feasible:
            findings.append(RiskFinding(
                factor="Schedule Buffer",
                status=RiskStatus.EVALUATED,
                finding="High Risk: Estimated schedule exceeds delivery deadline."
            ))
        else:
            findings.append(RiskFinding(
                factor="Schedule Buffer",
                status=RiskStatus.EVALUATED,
                finding="Low Risk: Estimated schedule meets delivery deadline."
            ))
    else:
        findings.append(RiskFinding(
            factor="Schedule Buffer",
            status=RiskStatus.INSUFFICIENT_DATA,
            finding="Cannot assess schedule risk.",
            missing_info="Transit time, loading rate, and port delays."
        ))
        
    # 3. Cost Certainty Risk
    if cost_is_complete:
        findings.append(RiskFinding(
            factor="Cost Certainty",
            status=RiskStatus.EVALUATED,
            finding="Low Risk: All required cost components are accounted for."
        ))
    else:
        findings.append(RiskFinding(
            factor="Cost Certainty",
            status=RiskStatus.EVALUATED,
            finding="High Risk: Voyage cost is partial or missing key components. Budget overrun is possible."
        ))

    # 4. Weather / Market Risk (Explicitly unsupported)
    findings.append(RiskFinding(
        factor="Weather and Market Volatility",
        status=RiskStatus.NOT_EVALUATED,
        finding="Not evaluated in this phase.",
        missing_info="Live weather routing API and market volatility indices."
    ))

    return RiskAssessmentReport(findings=findings)
