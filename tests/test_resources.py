def test_create_resource(client):
    response = client.post(
        "/resources/",
        json={
            "name": "Test VM",
            "resource_type": "vm",
            "cpu_cores": 4,
            "memory_gb": 8,
            "storage_gb": 100,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] is not None
    assert data["name"] == "Test VM"
    assert data["resource_type"] == "vm"
    assert data["cpu_cores"] == 4
    assert data["memory_gb"] == 8
    assert data["storage_gb"] == 100
    assert data["status"] == "running"


def test_get_resources(client):
    client.post(
        "/resources/",
        json={
            "name": "Test VM",
            "resource_type": "vm",
            "cpu_cores": 4,
            "memory_gb": 8,
            "storage_gb": 100,
        },
    )

    response = client.get("/resources/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Test VM"


def test_get_resource(client):
    create_response = client.post(
        "/resources/",
        json={
            "name": "Test VM",
            "resource_type": "vm",
            "cpu_cores": 4,
            "memory_gb": 8,
            "storage_gb": 100,
        },
    )

    resource_id = create_response.json()["id"]

    response = client.get(f"/resources/{resource_id}")

    assert response.status_code == 200
    assert response.json()["id"] == resource_id
    assert response.json()["name"] == "Test VM"


def test_update_resource(client):
    create_response = client.post(
        "/resources/",
        json={
            "name": "Test VM",
            "resource_type": "vm",
            "cpu_cores": 4,
            "memory_gb": 8,
            "storage_gb": 100,
        },
    )

    resource_id = create_response.json()["id"]

    response = client.put(
        f"/resources/{resource_id}",
        json={
            "name": "Updated VM",
            "cpu_cores": 8,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == resource_id
    assert data["name"] == "Updated VM"
    assert data["cpu_cores"] == 8


def test_delete_resource(client):
    create_response = client.post(
        "/resources/",
        json={
            "name": "Test VM",
            "resource_type": "vm",
            "cpu_cores": 4,
            "memory_gb": 8,
            "storage_gb": 100,
        },
    )

    resource_id = create_response.json()["id"]

    response = client.delete(f"/resources/{resource_id}")

    assert response.status_code == 204

    get_response = client.get(f"/resources/{resource_id}")

    assert get_response.status_code == 404

def test_get_nonexistent_resource(client):
    response = client.get("/resources/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Resource not found"

def test_create_resource_invalid_cpu(client):
    response = client.post(
        "/resources/",
        json={
            "name": "Invalid VM",
            "resource_type": "vm",
            "cpu_cores": 0,
            "memory_gb": 8,
            "storage_gb": 100,
        },
    )

    assert response.status_code == 422


def test_create_resource_empty_name(client):
    response = client.post(
        "/resources/",
        json={
            "name": "",
            "resource_type": "vm",
            "cpu_cores": 4,
            "memory_gb": 8,
            "storage_gb": 100,
        },
    )

    assert response.status_code == 422