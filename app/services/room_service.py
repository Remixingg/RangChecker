import requests
from flask import current_app
from ..utils import get_today_date
from ..models import Room

class RoomService:
    
    def __init__(self):
        self.api_url = None
        
    def initialize(self, app):
        self.api_url = app.config.get('ROOM_TRANSACTION_URL')
        if not self.api_url:
            app.logger.warning("ROOM_TRANSACTION_URL not configured")
    
    def get_available_rooms(self):
        # all available rooms
        if not self.api_url:
            current_app.logger.error("ROOM_TRANSACTION_URL not configured")
            return None
            
        today = get_today_date()
        
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
            current_app.logger.debug(f"Fetching room data from: {self.api_url}")
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # raw -> Room
            rooms = []
            for room_data in data.get("Details", []):
                campus = room_data.get("Campus", "")
                room_name = room_data.get("RoomName", "")
                status_details = room_data.get("StatusDetails", [])
                
                rooms.append(Room(room_name, campus, status_details))
                
            return rooms
        except Exception as e:
            current_app.logger.error(f"Error fetching room data: {str(e)}")
            return None
            
    def get_available_anggrek_rooms(self):
        # ANGGREK only
        excluded_rooms = {"329", "711A", "724", "724 Meeting Room", "728", "730", "731"}
        
        all_rooms = self.get_available_rooms()
        if not all_rooms:
            return None
            
        anggrek_rooms = [room for room in all_rooms 
                        if room.campus == "ANGGREK" and room.name not in excluded_rooms]
        
        return anggrek_rooms
        
    def get_room_availability_summary(self):
        rooms = self.get_available_anggrek_rooms()
        if not rooms:
            return None, None, None
            
        fully_available = []
        partially_available = []
        room_shift_details = {}
        
        for room in rooms:
            shift_status = room.get_shift_availability_status()
            room_shift_details[room.name] = shift_status
            
            if room.is_fully_available:
                fully_available.append(room.name)
            else:
                longest_streak = room.get_longest_available_streak()
                if longest_streak:
                    partially_available.append(room.name)
                    
        return fully_available, partially_available, room_shift_details


room_service = RoomService()