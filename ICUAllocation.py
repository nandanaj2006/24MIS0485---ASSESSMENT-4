class ICUAllocationSystem:
    def __init__(self, total_beds=5):
        self.total_beds = total_beds
        self.allocated_patients = {}
        self.waiting_list = []
        self.patient_records = set()

    def calculate_priority(self, age, oxygen, heart_rate, bp_sys, temp, is_emergency):
        score = 0
        if is_emergency:
            score += 100
        if oxygen < 85:
            score += 50
        elif oxygen < 92:
            score += 30
        if heart_rate > 120 or heart_rate < 50:
            score += 25
        if bp_sys < 90 or bp_sys > 180:
            score += 20
        if age > 65:
            score += 15
        if temp > 103.0:
            score += 10

        if score >= 80:
            category = "CRITICAL"
        elif score >= 50:
            category = "HIGH"
        elif score >= 25:
            category = "MEDIUM"
        else:
            category = "LOW"

        return score, category

    def admit_patient(self, patient_id, age, oxygen, heart_rate, bp_sys, temp, conditions, is_emergency=False):
        if patient_id in self.patient_records:
            return {"status": "REJECTED", "reason": "Duplicate patient ID."}
        if not (0 <= oxygen <= 100) or heart_rate <= 0:
            return {"status": "REJECTED", "reason": "Invalid vitals recorded."}

        self.patient_records.add(patient_id)
        score, category = self.calculate_priority(age, oxygen, heart_rate, bp_sys, temp, is_emergency)
        patient_data = {"id": patient_id, "score": score, "category": category, "is_emergency": is_emergency}

        if len(self.allocated_patients) < self.total_beds:
            self.allocated_patients[patient_id] = patient_data
            return {"status": "ALLOCATED", "patient_id": patient_id, "category": category, "score": score}
        else:
            # Bed override for emergencies against lower priorities
            if is_emergency:
                lowest = min(self.allocated_patients.values(), key=lambda p: p["score"])
                if lowest["score"] < score:
                    del self.allocated_patients[lowest["id"]]
                    self.waiting_list.append(lowest)
                    self.allocated_patients[patient_id] = patient_data
                    return {"status": "ALLOCATED_OVERRIDE", "displaced": lowest["id"], "category": category}

            self.waiting_list.append(patient_data)
            self.waiting_list.sort(key=lambda p: p["score"], reverse=True)
            return {"status": "WAITLISTED", "patient_id": patient_id, "category": category, "score": score}
