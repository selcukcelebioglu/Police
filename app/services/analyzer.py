import re
from dataclasses import dataclass

from app.services.legal import VIOLATION_LEGAL_MAP, VIOLATION_SUMMARY_MAP

SUPPORTED_VIOLATIONS = set(VIOLATION_LEGAL_MAP.keys())


@dataclass
class AnalysisResult:
    media_filename: str
    media_type: str
    detected_plate: str
    detected_vehicle_model: str
    detected_violation_type: str
    confidence_score: float
    legal_references: list[str]
    pre_report_summary: str


def detect_media_type(filename: str) -> str:
    lowered = filename.lower()
    if lowered.endswith((".jpg", ".jpeg", ".png", ".webp")):
        return "image"
    if lowered.endswith((".mp4", ".avi", ".mov", ".mkv")):
        return "video"
    return "unknown"


def normalize_plate(raw_plate: str) -> str:
    plate = re.sub(r"[^A-Za-z0-9]", "", raw_plate).upper()
    return plate[:16] if plate else "TESPIT_EDILEMEDI"


def heuristic_analyze(filename: str) -> AnalysisResult:
    name_no_ext = filename.rsplit(".", maxsplit=1)[0]
    tokens = name_no_ext.split("_")

    detected_plate = "TESPIT_EDILEMEDI"
    detected_vehicle_model = "BELIRSIZ"
    detected_violation = "generic_violation"

    if tokens:
        maybe_plate = normalize_plate(tokens[0])
        if re.match(r"^[0-9]{2}[A-Z]{1,3}[0-9]{2,4}$", maybe_plate):
            detected_plate = maybe_plate

    if len(tokens) > 1 and tokens[1].strip():
        detected_vehicle_model = tokens[1].strip()

    if len(tokens) > 2:
        maybe_violation = tokens[2].strip().lower()
        if maybe_violation in SUPPORTED_VIOLATIONS:
            detected_violation = maybe_violation

    confidence = 0.91 if detected_violation != "generic_violation" else 0.74

    return AnalysisResult(
        media_filename=filename,
        media_type=detect_media_type(filename),
        detected_plate=detected_plate,
        detected_vehicle_model=detected_vehicle_model,
        detected_violation_type=detected_violation,
        confidence_score=confidence,
        legal_references=VIOLATION_LEGAL_MAP[detected_violation],
        pre_report_summary=VIOLATION_SUMMARY_MAP[detected_violation],
    )
