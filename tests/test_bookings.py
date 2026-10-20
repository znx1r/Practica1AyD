import pytest


@pytest.fixture
def setup_room(client):
    client.post(
        "/rooms",
        json={"nombre": "Lab", "edificio": "A", "capacidad": 20, "equipamiento": []},
    )


def test_create_booking(client, setup_room):
    response = client.post(
        "/bookings",
        json={
            "aula_id": 1,
            "usuario": "Julian",
            "fecha": "2026-10-25",
            "hora_inicio": "10:00",
            "hora_fin": "12:00",
        },
    )
    assert response.status_code == 201
    assert response.json["id"] == 1


def test_booking_nonexistent_room(client):
    response = client.post(
        "/bookings",
        json={
            "aula_id": 99,
            "usuario": "Julian",
            "fecha": "2026-10-25",
            "hora_inicio": "10:00",
            "hora_fin": "12:00",
        },
    )
    assert response.status_code == 400
    assert response.json["error"] == "Aula inexistente"


def test_booking_invalid_time(client, setup_room):
    response = client.post(
        "/bookings",
        json={
            "aula_id": 1,
            "usuario": "Julian",
            "fecha": "2026-10-25",
            "hora_inicio": "13:00",
            "hora_fin": "12:00",
        },
    )
    assert response.status_code == 400


def test_booking_overlap(client, setup_room):
    # Reserva inicial
    client.post(
        "/bookings",
        json={
            "aula_id": 1,
            "usuario": "User1",
            "fecha": "2026-10-25",
            "hora_inicio": "10:00",
            "hora_fin": "12:00",
        },
    )

    # Intento de solapamiento
    response = client.post(
        "/bookings",
        json={
            "aula_id": 1,
            "usuario": "User2",
            "fecha": "2026-10-25",
            "hora_inicio": "11:00",
            "hora_fin": "13:00",
        },
    )
    assert response.status_code == 400
    assert response.json["error"] == "Reserva solapada"
