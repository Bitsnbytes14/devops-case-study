from app.main import app
from tests.test_engine import student
def test_health_and_sample():
    client = app.test_client(); assert client.get("/health").status_code == 200; assert client.get("/api/v1/sample").status_code == 200
def test_compatibility_and_bad_input():
    client = app.test_client(); response = client.post("/api/v1/compatibility", json={"first": student("a"), "second": student("b")}); assert response.status_code == 200 and response.json["valid"]
    assert client.post("/api/v1/allocate", json={"students": []}).status_code == 400
