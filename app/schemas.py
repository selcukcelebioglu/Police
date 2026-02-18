from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class AnalyzeResponse(BaseModel):
    media_filename: str
    media_type: Literal["image", "video", "unknown"]
    detected_plate: str
    detected_vehicle_model: str
    detected_violation_type: str
    confidence_score: float
    legal_references: list[str]
    pre_report_summary: str


class SubmitReportRequest(BaseModel):
    citizen_tc: str = Field(min_length=11, max_length=11)
    citizen_phone: str = Field(min_length=10, max_length=15)
    city: str | None = None
    district: str | None = None
    declaration_accepted: bool
    truth_statement_accepted: bool

    media_filename: str
    media_type: Literal["image", "video", "unknown"]
    detected_plate: str
    detected_vehicle_model: str
    detected_violation_type: str
    confidence_score: float
    legal_references: list[str]
    pre_report_summary: str

    @field_validator("citizen_tc")
    @classmethod
    def tc_only_digits(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("TCKN yalnızca rakamlardan oluşmalıdır.")
        return value


class ReportResponse(BaseModel):
    id: int
    citizen_tc: str
    citizen_phone: str
    city: str
    district: str
    media_filename: str
    media_type: str
    plate_number: str
    vehicle_model: str
    violation_type: str
    confidence_score: float
    legal_references: list[str]
    pre_report_summary: str
    status: str
    admin_notes: str
    final_decision: str
    created_at: datetime
    finalized_at: datetime | None

    class Config:
        from_attributes = True


class FinalizeReportRequest(BaseModel):
    final_decision: Literal["approved", "rejected"]
    admin_notes: str = Field(min_length=3)


class StatsResponse(BaseModel):
    by_city: dict[str, int]
    by_district: dict[str, int]
    by_vehicle_model: dict[str, int]
    by_violation_type: dict[str, int]
