from app.main import app
from tests.test_engine import student
def test_health_and_sample():
    client = app.test_client(); assert client.get("/health").status_code == 200; assert client.get("/api/v1/sample").status_code == 200
def test_compatibility_and_bad_input():
    client = app.test_client(); response = client.post("/api/v1/compatibility", json={"first": student("a"), "second": student("b")}); assert response.status_code == 200 and response.json["valid"]
    assert client.post("/api/v1/allocate", json={"students": []}).status_code == 400


def test_root_ready_validate_and_allocation():
    client = app.test_client()
    assert client.get("/").status_code == 200
    assert client.get("/ready").status_code == 200
    first, second = student("a"), student("b", smoking=True)
    response = client.post("/api/v1/validate", json={"students": [first, second]})
    assert response.status_code == 200 and not response.json["valid"]
    response = client.post(
        "/api/v1/allocate", json={"students": [student("a"), student("b")]}
    )
    assert response.status_code == 200 and response.json["students_allocated"] == 2


def test_validation_errors_and_metrics():
    client = app.test_client()
    assert client.post("/api/v1/validate", json={"students": []}).status_code == 400
    assert client.post(
        "/api/v1/compatibility", json={"first": {}, "second": {}}
    ).status_code == 400
    assert client.get("/metrics").status_code == 200
