import io
import pytest
from PIL import Image

pytestmark = pytest.mark.asyncio


def create_dummy_leaf_image() -> bytes:
    """Create a green RGB test image representing a crop leaf."""
    img = Image.new("RGB", (224, 224), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


async def test_health_check(client):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "version" in data


async def test_models_health(client):
    response = await client.get("/api/v1/health/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert "disease_classifier" in data["models"]


async def test_auth_workflow(client):
    unique_phone = "9988776655"
    # Register
    reg_payload = {
        "full_name": "Test Farmer",
        "phone": unique_phone,
        "password": "SecretPassword123",
        "preferred_language": "mr",
        "preferred_theme": "light"
    }
    reg_res = await client.post("/api/v1/auth/register", json=reg_payload)
    if reg_res.status_code == 400:
        # Already registered, proceed to login
        pass
    else:
        assert reg_res.status_code == 201
        data = reg_res.json()
        assert "access_token" in data

    # Login
    login_payload = {
        "phone": unique_phone,
        "password": "SecretPassword123"
    }
    login_res = await client.post("/api/v1/auth/login", json=login_payload)
    assert login_res.status_code == 200
    login_data = login_res.json()
    token = login_data["access_token"]
    assert token is not None

    # Get Me
    headers = {"Authorization": f"Bearer {token}"}
    me_res = await client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["phone"] == unique_phone


async def test_weather_endpoints(client):
    res = await client.get("/api/v1/weather/current?district=Pune&state=Maharashtra")
    assert res.status_code == 200
    data = res.json()
    assert "temperature_celsius" in data
    assert "agricultural_advisories" in data

    forecast_res = await client.get("/api/v1/weather/forecast?district=Pune&days=3")
    assert forecast_res.status_code == 200
    forecast_data = forecast_res.json()
    assert len(forecast_data) == 3


async def test_recommendations(client):
    res = await client.get("/api/v1/recommendations/Tomato Early Blight?language=en")
    assert res.status_code == 200
    data = res.json()
    assert "chemical_control" in data
    assert "organic_control" in data


async def test_knowledge_base(client):
    cat_res = await client.get("/api/v1/knowledge/categories")
    assert cat_res.status_code == 200

    art_res = await client.get("/api/v1/knowledge/")
    assert art_res.status_code == 200
    art_data = art_res.json()
    assert "items" in art_data


async def test_yield_prediction(client):
    payload = {
        "crop": "Tomato",
        "district": "Pune",
        "season": "Kharif",
        "area_hectares": 2.0,
        "soil_type": "Black Soil",
        "irrigation": True
    }
    res = await client.post("/api/v1/yield/predict", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["predicted_yield_kg_per_hectare"] > 0
    assert data["predicted_total_production_kg"] > 0


async def test_diagnosis_flow(client):
    leaf_bytes = create_dummy_leaf_image()
    files = {"image": ("test_leaf.jpg", leaf_bytes, "image/jpeg")}
    data = {"crop_type": "Tomato", "language": "en"}

    diag_res = await client.post("/api/v1/diagnosis/", files=files, data=data)
    assert diag_res.status_code == 201
    diag_data = diag_res.json()
    assert "id" in diag_data
    assert "predicted_disease" in diag_data
    assert "severity" in diag_data
    assert "recommendations" in diag_data

    # Generate Report for this diagnosis
    report_res = await client.post(f"/api/v1/reports/generate/{diag_data['id']}")
    assert report_res.status_code == 201
    rep_data = report_res.json()
    assert "report_url" in rep_data
