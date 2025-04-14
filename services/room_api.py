import requests
from utils.date_utils import get_today_date

class RoomAPI:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_available_rooms(self):
        today = get_today_date()
        # today = "04/15/2025"

        params = {
            "startDate": today,
            "endDate": today,
            "includeUnapproved": True,
            "includeOnsiteData": True,
            "campuses": ["ANGGREK"],
            "assistants": [],
            "description": "",
            "roomNames": []
        }

        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()

            # Print for now for debugging
            print("Room API Response:", data)

            return data
        except Exception as e:
            print(f"Error fetching room data: {e}")
            return None

    def parse_available_rooms(self, data):
        available_rooms = []
        # unavailable_rooms = []

        for room in data.get("Details", []):
            # ANGGREK only
            campus = room.get("Campus", "")
            if campus != "ANGGREK":
                continue

            room_name = room.get("RoomName", "")
            status_details = room.get("StatusDetails", [])

            is_unavailable = any(status for status in status_details)

            if not is_unavailable:
                available_rooms.append(room_name)
            # else:
            #     unavailable_rooms.append(room_name)

        print("Available Rooms:")
        for room in available_rooms:
            print(f"- {room}")

        # print("\nUnavailable Rooms:")
        # for room in unavailable_rooms:
        #     print(f"- {room}")

        return available_rooms

