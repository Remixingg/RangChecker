class Room:
    """Model representing a room and its availability."""
    
    def __init__(self, name, campus, status_details=None):
        self.name = name
        self.campus = campus
        self.status_details = status_details or []
        
    @property
    def is_fully_available(self):
        """Check if room is fully available across all shifts."""
        shift_indices = [1, 3, 5, 7, 9, 11]
        shifts = [self.status_details[i] if i < len(self.status_details) else [] for i in shift_indices]
        return all(len(shift) == 0 for shift in shifts)
    
    def get_available_shifts(self):
        """Get list of available shift numbers."""
        shift_indices = [1, 3, 5, 7, 9, 11]
        return [i+1 for i, idx in enumerate(shift_indices) 
                if idx < len(self.status_details) and len(self.status_details[idx]) == 0]
    
    def get_longest_available_streak(self):
        """Get the longest consecutive streak of available shifts."""
        available_shifts = self.get_available_shifts()
        if not available_shifts:
            return []
            
        streaks = []
        temp = []

        for i in range(len(available_shifts)):
            if not temp:
                temp.append(available_shifts[i])
            elif available_shifts[i] == temp[-1] + 1:
                temp.append(available_shifts[i])
            else:
                if len(temp) >= 3:  # 3 shifts continuously empty
                    streaks.append(temp)
                temp = [available_shifts[i]]
                
        if len(temp) >= 3:
            streaks.append(temp)

        return max(streaks, key=len) if streaks else []