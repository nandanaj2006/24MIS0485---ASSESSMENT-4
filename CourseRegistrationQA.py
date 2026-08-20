import unittest
from CourseRegistration import CourseRegistration

class TestCourseRegistration(unittest.TestCase):
    def setUp(self):
        self.system = CourseRegistration(max_credits=10)

    def test_valid_registration(self):
        res = self.system.register_courses("S101", "BTech", 4, ["DBMS", "Cloud"], ["Programming", "Networking"])
        self.assertEqual(res["status"], "APPROVED")
        self.assertEqual(res["total_credits"], 7)

    def test_missing_prerequisite(self):
        res = self.system.register_courses("S102", "BTech", 4, ["AI"], [])
        self.assertEqual(res["status"], "REJECTED")
        self.assertIn("Prerequisite", res["reason"])

    def test_timetable_conflict(self):
        # DBMS and ML share MON_09:00 slot
        res = self.system.register_courses("S103", "BTech", 4, ["DBMS", "ML"], ["Programming", "Statistics"])
        self.assertEqual(res["status"], "REJECTED")
        self.assertIn("Timetable conflict", res["reason"])

    def test_credit_limit_violation(self):
        sys = CourseRegistration(max_credits=5)
        res = sys.register_courses("S104", "BTech", 4, ["DBMS", "Cloud"], ["Programming", "Networking"])
        self.assertEqual(res["status"], "REJECTED")
        self.assertIn("Credit limit exceeded", res["reason"])

    def test_duplicate_registration(self):
        res = self.system.register_courses("S105", "BTech", 4, ["DBMS", "DBMS"], ["Programming"])
        self.assertEqual(res["status"], "REJECTED")

if __name__ == "__main__":
    unittest.main()
