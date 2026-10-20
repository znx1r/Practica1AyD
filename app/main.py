from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Almacenamiento en memoria
rooms = []
bookings = []
room_id_counter = 1
booking_id_counter = 1


# --- HEALTH ---
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


# --- ROOMS (Aulas) ---
@app.route("/rooms", methods=["POST"])
def create_room():
    global room_id_counter
    data = request.get_json()

    if not data or not all(
        k in data for k in ("nombre", "edificio", "capacidad", "equipamiento")
    ):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    if data["capacidad"] <= 0:
        return jsonify({"error": "La capacidad debe ser mayor que 0"}), 400

    new_room = {
        "id": room_id_counter,
        "nombre": data["nombre"],
        "edificio": data["edificio"],
        "capacidad": data["capacidad"],
        "equipamiento": data["equipamiento"],
    }
    rooms.append(new_room)
    room_id_counter += 1

    return jsonify(new_room), 201


@app.route("/rooms", methods=["GET"])
def get_rooms():
    return jsonify(rooms), 200


@app.route("/rooms/<int:room_id>", methods=["GET"])
def get_room(room_id):
    room = next((r for r in rooms if r["id"] == room_id), None)
    if room:
        return jsonify(room), 200
    return jsonify({"error": "Aula inexistente"}), 404


@app.route("/rooms/<int:room_id>", methods=["DELETE"])
def delete_room(room_id):
    global rooms
    room = next((r for r in rooms if r["id"] == room_id), None)
    if not room:
        return jsonify({"error": "Aula inexistente"}), 404

    rooms = [r for r in rooms if r["id"] != room_id]
    return "", 204


# --- BOOKINGS (Reservas) ---
@app.route("/bookings", methods=["POST"])
def create_booking():
    global booking_id_counter
    data = request.get_json()

    if not data or not all(
        k in data for k in ("aula_id", "usuario", "fecha", "hora_inicio", "hora_fin")
    ):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    # Validar que el aula existe
    if not any(r["id"] == data["aula_id"] for r in rooms):
        return jsonify({"error": "Aula inexistente"}), 400

    # Validar horas
    formato_hora = "%H:%M"
    try:
        inicio = datetime.strptime(data["hora_inicio"], formato_hora)
        fin = datetime.strptime(data["hora_fin"], formato_hora)
        if inicio >= fin:
            return (
                jsonify(
                    {"error": "La hora de inicio debe ser anterior a la hora de fin"}
                ),
                400,
            )
    except ValueError:
        return jsonify({"error": "Formato de hora incorrecto"}), 400

    # Validar solapamientos
    for b in bookings:
        if b["aula_id"] == data["aula_id"] and b["fecha"] == data["fecha"]:
            b_inicio = datetime.strptime(b["hora_inicio"], formato_hora)
            b_fin = datetime.strptime(b["hora_fin"], formato_hora)

            # Hay solapamiento si el inicio de una es antes del fin de la otra y viceversa
            if inicio < b_fin and fin > b_inicio:
                return jsonify({"error": "Reserva solapada"}), 400

    new_booking = {
        "id": booking_id_counter,
        "aula_id": data["aula_id"],
        "usuario": data["usuario"],
        "fecha": data["fecha"],
        "hora_inicio": data["hora_inicio"],
        "hora_fin": data["hora_fin"],
    }
    bookings.append(new_booking)
    booking_id_counter += 1

    return jsonify(new_booking), 201


@app.route("/bookings", methods=["GET"])
def get_bookings():
    return jsonify(bookings), 200


@app.route("/bookings/<int:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    global bookings
    booking = next((b for b in bookings if b["id"] == booking_id), None)
    if not booking:
        return jsonify({"error": "Reserva inexistente"}), 404

    bookings = [b for b in bookings if b["id"] != booking_id]
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
