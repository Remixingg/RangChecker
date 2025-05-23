from ..services import room_service
from ..utils import get_today_date

def generate_hello_response():
    return {
        "type": "text",
        "text": "Hello"
    }

def generate_rang_response():
    fully_available, partially_available, room_shift_details = room_service.get_room_availability_summary()
    
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
            shift_status = room_shift_details.get(room, [])
            # Check if room has any calibrations
            if 'calibration' in shift_status:
                calib_shifts = [str(i+1) for i, status in enumerate(shift_status) if status == 'calibration']
                calib_display = ', '.join(calib_shifts)
                message += f"- {room} (🟪 - {calib_display})\n"
            else:
                message += f"- {room}\n"
    else:
        message += "\nNo rooms are fully available at the moment."

    # PARTIAL
    if partially_available:
        message += "\nPartially Available Rangs:\n"
        for room in partially_available:
            shift_status = room_shift_details.get(room, [])
            shift_bar = ""
            
            for status in shift_status:
                if status == 'available':
                    shift_bar += "🟩"
                elif status == 'calibration':
                    shift_bar += "🟪"
                else:
                    shift_bar += "🟥"
                    
            message += f"- {room}: {shift_bar}\n"

    return {
        "type": "text",
        "text": message.strip()
    }