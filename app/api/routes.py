from datetime import datetime

from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import ViolationReport
from app.schemas import (
    AnalyzeResponse,
    FinalizeReportRequest,
    ReportResponse,
    StatsResponse,
    SubmitReportRequest,
)
from app.services.analyzer import heuristic_analyze
from app.services.location import resolve_location

router = APIRouter()


@router.post("/reports/analyze", response_model=AnalyzeResponse)
async def analyze_violation_media(file: UploadFile = File(...)) -> AnalyzeResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Dosya adı bulunamadı")

    analysis = heuristic_analyze(file.filename)
    return AnalyzeResponse(**analysis.__dict__)


@router.post("/reports/submit", response_model=ReportResponse)
def submit_pre_report(
    payload: SubmitReportRequest,
    db: Session = Depends(get_db),
    x_city: str | None = Header(default=None),
    x_district: str | None = Header(default=None),
) -> ReportResponse:
    if not payload.declaration_accepted or not payload.truth_statement_accepted:
        raise HTTPException(
            status_code=400,
            detail="Yasal beyan ve doğruluk onayları zorunludur.",
        )

    city, district = resolve_location(payload.city, payload.district, x_city, x_district)

    row = ViolationReport(
        citizen_tc=payload.citizen_tc,
        citizen_phone=payload.citizen_phone,
        city=city,
        district=district,
        declaration_accepted=payload.declaration_accepted,
        truth_statement_accepted=payload.truth_statement_accepted,
        media_filename=payload.media_filename,
        media_type=payload.media_type,
        plate_number=payload.detected_plate,
        vehicle_model=payload.detected_vehicle_model,
        violation_type=payload.detected_violation_type,
        confidence_score=payload.confidence_score,
        legal_references="\n".join(payload.legal_references),
        pre_report_summary=payload.pre_report_summary,
    )

    db.add(row)
    db.commit()
    db.refresh(row)

    return ReportResponse(
        id=row.id,
        citizen_tc=row.citizen_tc,
        citizen_phone=row.citizen_phone,
        city=row.city,
        district=row.district,
        media_filename=row.media_filename,
        media_type=row.media_type,
        plate_number=row.plate_number,
        vehicle_model=row.vehicle_model,
        violation_type=row.violation_type,
        confidence_score=row.confidence_score,
        legal_references=row.legal_references.splitlines(),
        pre_report_summary=row.pre_report_summary,
        status=row.status,
        admin_notes=row.admin_notes,
        final_decision=row.final_decision,
        created_at=row.created_at,
        finalized_at=row.finalized_at,
    )


@router.get("/admin/reports/pending", response_model=list[ReportResponse])
def list_pending_reports(db: Session = Depends(get_db)) -> list[ReportResponse]:
    pending = db.query(ViolationReport).filter(ViolationReport.status == "pending").all()
    return [
        ReportResponse(
            id=row.id,
            citizen_tc=row.citizen_tc,
            citizen_phone=row.citizen_phone,
            city=row.city,
            district=row.district,
            media_filename=row.media_filename,
            media_type=row.media_type,
            plate_number=row.plate_number,
            vehicle_model=row.vehicle_model,
            violation_type=row.violation_type,
            confidence_score=row.confidence_score,
            legal_references=row.legal_references.splitlines(),
            pre_report_summary=row.pre_report_summary,
            status=row.status,
            admin_notes=row.admin_notes,
            final_decision=row.final_decision,
            created_at=row.created_at,
            finalized_at=row.finalized_at,
        )
        for row in pending
    ]


@router.post("/admin/reports/{report_id}/finalize", response_model=ReportResponse)
def finalize_report(
    report_id: int,
    payload: FinalizeReportRequest,
    db: Session = Depends(get_db),
) -> ReportResponse:
    report = db.query(ViolationReport).filter(ViolationReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Rapor bulunamadı")

    report.status = "closed"
    report.final_decision = payload.final_decision
    report.admin_notes = payload.admin_notes
    report.finalized_at = datetime.utcnow()

    db.commit()
    db.refresh(report)

    return ReportResponse(
        id=report.id,
        citizen_tc=report.citizen_tc,
        citizen_phone=report.citizen_phone,
        city=report.city,
        district=report.district,
        media_filename=report.media_filename,
        media_type=report.media_type,
        plate_number=report.plate_number,
        vehicle_model=report.vehicle_model,
        violation_type=report.violation_type,
        confidence_score=report.confidence_score,
        legal_references=report.legal_references.splitlines(),
        pre_report_summary=report.pre_report_summary,
        status=report.status,
        admin_notes=report.admin_notes,
        final_decision=report.final_decision,
        created_at=report.created_at,
        finalized_at=report.finalized_at,
    )


@router.get("/stats/violations", response_model=StatsResponse)
def violation_stats(db: Session = Depends(get_db)) -> StatsResponse:
    def count_by(column_name: str) -> dict[str, int]:
        column = getattr(ViolationReport, column_name)
        rows = db.execute(select(column, func.count()).group_by(column)).all()
        return {k: v for k, v in rows}

    return StatsResponse(
        by_city=count_by("city"),
        by_district=count_by("district"),
        by_vehicle_model=count_by("vehicle_model"),
        by_violation_type=count_by("violation_type"),
    )
