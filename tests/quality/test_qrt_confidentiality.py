import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.mark.qrt
@pytest.mark.quality
def test_safe_error_confidentiality():
    client = TestClient(app)
    
    response = client.post(
        "/solve", 
        content=b"{this is not valid json syntax", 
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code in [400, 422]
    body = response.text
    assert "Traceback" not in body, "Stack trace leaked in 400 response"
    assert "/app/" not in body, "Internal file path leaked"
    
    response = client.get("/jobs/non-existent-uuid-12345")
    assert response.status_code == 404
    assert "Traceback" not in response.text