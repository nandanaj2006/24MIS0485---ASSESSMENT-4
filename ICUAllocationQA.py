import unittest
from ICUAllocation import ICUAllocationSystem

class TestICUAllocation(unittest.TestCase):
    def setUp(self):
        self.icu = ICUAllocationSystem(total_beds=2)

    def test_critical_patient(self):
        res = self.icu.admit_patient("P01", 70, 80, 130, 85, 104.0, ["Diabetes"])
        self.assertEqual(res["category"], "CRITICAL")
        self.assertEqual(res["status"], "ALLOCATED")

    def test_duplicate_patient(self):
        self.icu.admit_patient("P01", 30, 98, 72, 120, 98.6, [])
        res = self.icu.admit_patient("P01", 30, 98, 72, 120, 98.6, [])
        self.assertEqual(res["status"], "REJECTED")

    def test_invalid_vitals(self):
        res = self.icu.admit_patient("P02", 30, 105, 72, 120, 98.6, [])
        self.assertEqual(res["status"], "REJECTED")

    def test_bed_exhaustion_and_override(self):
        self.icu.admit_patient("P01", 30, 98, 72, 120, 98.6, []) # LOW
        self.icu.admit_patient("P02", 40, 97, 75, 120, 98.6, []) # LOW
        # 3rd normal patient -> waitlist
        res3 = self.icu.admit_patient("P03", 25, 96, 70, 120, 98.6, [])
        self.assertEqual(res3["status"], "WAITLISTED")
        # Emergency patient -> overrides lowest bed
        res_emg = self.icu.admit_patient("P04", 68, 80, 140, 80, 101.0, [], is_emergency=True)
        self.assertEqual(res_emg["status"], "ALLOCATED_OVERRIDE")

if __name__ == "__main__":
    unittest.main()
