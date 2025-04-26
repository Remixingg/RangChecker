import requests
from utils.date_utils import get_today_date

class RoomAPI:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_available_rooms(self):
        today = get_today_date()
        # today = "02/14/2025"

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

            return data
        except Exception as e:
            print(f"Error fetching room data: {e}")
            return None

    def parse_available_rooms(self, data):
        excluded_rooms = {"329", "711A", "724", "724 Meeting Room", "728", "730", "731"}
        fully_available = []
        partially_available = {}
        # available_rooms = []
        # unavailable_rooms = []

        for room in data.get("Details", []):
            # ANGGREK only
            campus = room.get("Campus", "")
            if campus != "ANGGREK":
                continue

            room_name = room.get("RoomName", "")
            if room_name in excluded_rooms:
                continue
            status_details = room.get("StatusDetails", [])

            shift_indices = [1, 3, 5, 7, 9, 11]
            shifts = [status_details[i] if i < len(status_details) else [] for i in shift_indices]

            if all(len(shift) == 0 for shift in shifts):
                fully_available.append(room_name)
            else:
                empty_shift_nums = [i+1 for i, shift in enumerate(shifts) if len(shift) == 0]
                streaks = []
                temp = []

                for i in range(len(empty_shift_nums)):
                    if not temp:
                        temp.append(empty_shift_nums[i])
                    elif empty_shift_nums[i] == temp[-1] + 1:
                        temp.append(empty_shift_nums[i])
                    else:
                        if len(temp) >= 3:
                            streaks.append(temp)
                        temp = [empty_shift_nums[i]]
                if len(temp) >= 3:
                    streaks.append(temp)

                if streaks:
                    longest_streak = max(streaks, key=len)
                    partially_available[room_name] = longest_streak

        return fully_available, partially_available

