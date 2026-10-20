def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_create_room(client):
    response = client.post(
        "/rooms",
        json={
            "nombre": "Laboratorio A",
            "edificio": "Norte",
            "capacidad": 30,
            "equipamiento": ["PCs"],
        },
    )
    assert response.status_code == 201
    assert response.json["id"] == 1


def test_create_room_invalid_capacity(client):
    response = client.post(
        "/rooms",
        json={"nombre": "Zulo", "edificio": "Sur", "capacidad": 0, "equipamiento": []},
    )
    assert response.status_code == 400
    assert "capacidad debe ser mayor que 0" in response.json["error"]


def test_get_rooms(client):
    client.post(
        "/rooms",
        json={"nombre": "A", "edificio": "B", "capacidad": 10, "equipamiento": []},
    )
    response = client.get("/rooms")
    assert response.status_code == 200
    assert len(response.json) == 1


def test_get_room_not_found(client):
    response = client.get("/rooms/999")
    assert response.status_code == 404
    assert response.json["error"] == "Aula inexistente"


def test_delete_room(client):
    client.post(
        "/rooms",
        json={"nombre": "A", "edificio": "B", "capacidad": 10, "equipamiento": []},
    )
    response = client.delete("/rooms/1")
    assert response.status_code == 204

    response_get = client.get("/rooms/1")
    assert response_get.status_code == 404
