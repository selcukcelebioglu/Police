from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_analyze_endpoint() -> None:
    response = client.post(
        "/api/reports/analyze",
        files={"file": ("34ABC123_ToyotaCorolla_redlight.jpg", b"dummy", "image/jpeg")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["detected_plate"] == "34ABC123"
    assert body["detected_violation_type"] == "redlight"


def test_submit_and_finalize_flow() -> None:
    submit_payload = {
        "citizen_tc": "12345678901",
        "citizen_phone": "05551234567",
        "city": "İstanbul",
        "district": "Kadıköy",
        "declaration_accepted": True,
        "truth_statement_accepted": True,
        "media_filename": "34ABC123_ToyotaCorolla_redlight.jpg",
        "media_type": "image",
        "detected_plate": "34ABC123",
        "detected_vehicle_model": "ToyotaCorolla",
        "detected_violation_type": "redlight",
        "confidence_score": 0.92,
        "legal_references": ["Kanun m.47"],
        "pre_report_summary": "Kırmızı ışık ihlali şüphesi.",
    }

    submit = client.post("/api/reports/submit", json=submit_payload)
    assert submit.status_code == 200
    report_id = submit.json()["id"]

    pending = client.get("/api/admin/reports/pending")
    assert pending.status_code == 200
    assert any(row["id"] == report_id for row in pending.json())

    finalize = client.post(
        f"/api/admin/reports/{report_id}/finalize",
        json={"final_decision": "approved", "admin_notes": "Polis onayı verildi"},
    )
    assert finalize.status_code == 200
    assert finalize.json()["status"] == "closed"


def test_stats_endpoint() -> None:
    response = client.get("/api/stats/violations")
    assert response.status_code == 200
    body = response.json()
    assert "by_city" in body
    assert "by_violation_type" in body
