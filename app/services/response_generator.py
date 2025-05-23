from ..services import room_service
from ..utils import get_today_date

def generate_hello_response():
    return {
        "type": "text",
        "text": "Hello"
    }

def generate_rang_response():
    fully_available, partially_available, calibration_info = room_service.get_room_availability_summary()
    
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
        for room in fully_available:
            if room in calibration_info:
                calib_shifts = calibration_info[room]
                calib_display = ', '.join(map(str, calib_shifts))
                message += f"- {room} (🟪 - {calib_display})\n"
            else:
                message += f"- {room}\n"
    else:
        message += "\nNo rooms are fully available at the moment."

    # PARTIAL
    if partially_available:
        message += "\nPartially Available Rangs:\n"
        for room, shifts in partially_available.items():
            shift_bar = ""
            calib_shifts = calibration_info.get(room, [])
            
            for i in range(1, 7):
                if i in shifts:
                    if i in calib_shifts:
                        shift_bar += "🟪"
                    else:
                        shift_bar += "🟩"
                else:
                    shift_bar += "🟥"
                    
            message += f"- {room}: {shift_bar}\n"

    return {
        "type": "text",
        "text": message.strip()
    }