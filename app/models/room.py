class Room:
    
    def __init__(self, name, campus, status_details=None):
        self.name = name
        self.campus = campus
        self.status_details = status_details or []
        
    def _is_calibration_transaction(self, transaction):
        return "CALIB-Calibration" in transaction.get("Description", "")
    
    def _get_non_calibration_transactions(self, shift_transactions):
        return [t for t in shift_transactions if not self._is_calibration_transaction(t)]
    
    def _get_calibration_shifts(self):
        shift_indices = [1, 3, 5, 7, 9, 11]
        calibration_shifts = []
        
        for i, idx in enumerate(shift_indices):
            if idx < len(self.status_details):
                shift_transactions = self.status_details[idx]
                if any(self._is_calibration_transaction(t) for t in shift_transactions):
                    calibration_shifts.append(i + 1) 
        
        return calibration_shifts
        
    @property
    def is_fully_available(self):
        shift_indices = [1, 3, 5, 7, 9, 11]
        for idx in shift_indices:
            if idx < len(self.status_details):
                non_calib_transactions = self._get_non_calibration_transactions(self.status_details[idx])
                if len(non_calib_transactions) > 0:
                    return False
        return True
    
    def get_available_shifts(self):
        shift_indices = [1, 3, 5, 7, 9, 11]
        available_shifts = []
        
        for i, idx in enumerate(shift_indices):
            if idx < len(self.status_details):
                non_calib_transactions = self._get_non_calibration_transactions(self.status_details[idx])
                if len(non_calib_transactions) == 0:
                    available_shifts.append(i + 1)
            else:
                available_shifts.append(i + 1)
                
        return available_shifts
    
    def get_longest_available_streak(self):
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
    
    def get_calibration_info(self):
        return {
            'has_calibrations': len(self._get_calibration_shifts()) > 0,
            'calibration_shifts': self._get_calibration_shifts()
        }