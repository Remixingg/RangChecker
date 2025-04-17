from services.room_api import RoomAPI
from settings import dev
from datetime import datetime

room_api = RoomAPI(dev.ROOM_TRANSACTION_URL)

def handle_rang():
    rooms = room_api.get_available_rooms()

    if not rooms:
        return "Failed to fetch room transactions"
    
    fully_available, partially_available = room_api.parse_available_rooms(rooms)

    today = datetime.now()
    day_date_str = today.strftime("%A, %d %B %Y")
    message = f"{day_date_str}\n-----------------------------\n"

    # FULL
    if fully_available:
        message += "Available Rangs:\n"
        message += '\n'.join(f"- {room}" for room in fully_available)
    else:
        message += "\nNo rooms are fully available at the moment."

    # PARTIAL
    if partially_available:
        message += "\nPartially Available Rangs:\n"
        for room, shifts in partially_available.items():
            shift_bar = ""
            for i in range(1, 7):
                if i in shifts:
                    shift_bar += "🟩"
                else:
                    shift_bar += "🟥"
            # shift_range = f"Shift {shifts[0]}–{shifts[-1]}" if len(shifts) > 1 else f"Shift {shifts[0]}"
            # message += f"- {room}: {shift_bar} {shift_range}\n"
            message += f"- {room}: {shift_bar}\n"

    return message.strip()

