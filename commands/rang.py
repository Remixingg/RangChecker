from services.room_api import RoomAPI
from settings import dev
from datetime import datetime

room_api = RoomAPI(dev.ROOM_TRANSACTION_URL)

def handle_rang():
    rooms = room_api.get_available_rooms()

    if not rooms:
        return "Failed to fetch room transactions"
    else:
        available_rooms = room_api.parse_available_rooms(rooms)

        today = datetime.now()
        day_date_str = today.strftime("%A, %d %B %Y")

        if available_rooms:
            rooms_text = '\n'.join(f"- {room}" for room in available_rooms)
            reply_message = f"{day_date_str}\nAvailable Rangs:\n{rooms_text}"
        else:
            reply_message = f"{day_date_str}\nNo rooms are available at the moment."

    return reply_message

