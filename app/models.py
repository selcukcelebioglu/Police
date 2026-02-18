from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class ViolationReport(Base):
    __tablename__ = "violation_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    citizen_tc: Mapped[str] = mapped_column(String(11), index=True)
    citizen_phone: Mapped[str] = mapped_column(String(15))
    city: Mapped[str] = mapped_column(String(64), index=True)
    district: Mapped[str] = mapped_column(String(64), index=True)
    declaration_accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    truth_statement_accepted: Mapped[bool] = mapped_column(Boolean, default=False)

    media_filename: Mapped[str] = mapped_column(String(255))
    media_type: Mapped[str] = mapped_column(String(16))
    plate_number: Mapped[str] = mapped_column(String(16), index=True)
    vehicle_model: Mapped[str] = mapped_column(String(128), index=True)
    violation_type: Mapped[str] = mapped_column(String(64), index=True)
    confidence_score: Mapped[float] = mapped_column(Float)
    legal_references: Mapped[str] = mapped_column(Text)
    pre_report_summary: Mapped[str] = mapped_column(Text)

    status: Mapped[str] = mapped_column(String(16), default="pending", index=True)
    admin_notes: Mapped[str] = mapped_column(Text, default="")
    final_decision: Mapped[str] = mapped_column(String(16), default="pending")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finalized_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
