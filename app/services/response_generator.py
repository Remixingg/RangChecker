from ..services import room_service
from ..utils import get_today_date

def generate_hello_response():
    return {
        "type": "text",
        "text": "Hello"
    }

def generate_rang_response():
    fully_available, partially_available = room_service.get_room_availability_summary()
    
    if fully_available is None:
        return {
            "type": "text",
            "text": "Failed to fetch room availability information."
        }
    
    day_date_str = get_today_date()
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
            message += f"- {room}: {shift_bar}\n"

    return {
        "type": "text",
        "text": message.strip()
    }