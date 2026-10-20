import pytest
from app.main import app as flask_app, rooms, bookings
import app.main


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_state():
    """Resetea las listas en memoria antes de cada test."""
    rooms.clear()
    bookings.clear()
    app.main.room_id_counter = 1
    app.main.booking_id_counter = 1
