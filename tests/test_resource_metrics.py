def test_create_metric(client):
    resource_response = client.post(
        "/resources/",
        json={
            "name": "Metrics VM",
            "resource_type": "vm",
            "cpu_cores": 4,
            "memory_gb": 8,
            "storage_gb": 100,
        },
    )

    resource_id = resource_response.json()["id"]

    response = client.post(
        f"/resources/{resource_id}/metrics",
        json={
            "cpu_usage_percent": 45.5,
            "memory_usage_percent": 60,
            "storage_usage_percent": 30,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["resource_id"] == resource_id
    assert data["cpu_usage_percent"] == 45.5
    assert data["memory_usage_percent"] == 60
    assert data["storage_usage_percent"] == 30
    assert "recorded_at" in data


def test_get_metrics(client):
    resource_response = client.post(
        "/resources/",
        json={
            "name": "Metrics VM",
            "resource_type": "vm",
            "cpu_cores": 4,
            "memory_gb": 8,
            "storage_gb": 100,
        },
    )

    resource_id = resource_response.json()["id"]

    client.post(
        f"/resources/{resource_id}/metrics",
        json={
            "cpu_usage_percent": 40,
            "memory_usage_percent": 50,
            "storage_usage_percent": 20,
        },
    )

    client.post(
        f"/resources/{resource_id}/metrics",
        json={
            "cpu_usage_percent": 70,
            "memory_usage_percent": 80,
            "storage_usage_percent": 40,
        },
    )

    response = client.get(
        f"/resources/{resource_id}/metrics"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["cpu_usage_percent"] == 70
    assert data[1]["cpu_usage_percent"] == 40


def test_get_latest_metric(client):
    resource_response = client.post(
        "/resources/",
        json={
            "name": "Latest Metrics VM",
            "resource_type": "vm",
            "cpu_cores": 4,
            "memory_gb": 8,
            "storage_gb": 100,
        },
    )

    resource_id = resource_response.json()["id"]

    client.post(
        f"/resources/{resource_id}/metrics",
        json={
            "cpu_usage_percent": 30,
            "memory_usage_percent": 40,
            "storage_usage_percent": 20,
        },
    )

    client.post(
        f"/resources/{resource_id}/metrics",
        json={
            "cpu_usage_percent": 90,
            "memory_usage_percent": 85,
            "storage_usage_percent": 70,
        },
    )

    response = client.get(
        f"/resources/{resource_id}/metrics/latest"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["cpu_usage_percent"] == 90
    assert data["memory_usage_percent"] == 85
    assert data["storage_usage_percent"] == 70


def test_create_metric_invalid_percentage(client):
    resource_response = client.post(
        "/resources/",
        json={
            "name": "Invalid Metrics VM",
            "resource_type": "vm",
            "cpu_cores": 4,
            "memory_gb": 8,
            "storage_gb": 100,
        },
    )

    resource_id = resource_response.json()["id"]

    response = client.post(
        f"/resources/{resource_id}/metrics",
        json={
            "cpu_usage_percent": 120,
            "memory_usage_percent": 50,
            "storage_usage_percent": 30,
        },
    )

    assert response.status_code == 422


def test_create_metric_nonexistent_resource(client):
    response = client.post(
        "/resources/99999/metrics",
        json={
            "cpu_usage_percent": 50,
            "memory_usage_percent": 50,
            "storage_usage_percent": 50,
        },
    )

    assert response.status_code == 404


def test_get_latest_metric_when_none_exist(client):
    resource_response = client.post(
        "/resources/",
        json={
            "name": "No Metrics VM",
            "resource_type": "vm",
            "cpu_cores": 4,
            "memory_gb": 8,
            "storage_gb": 100,
        },
    )

    resource_id = resource_response.json()["id"]

    response = client.get(
        f"/resources/{resource_id}/metrics/latest"
    )

    assert response.status_code == 404