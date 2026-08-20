class CourseRegistration:
    COURSE_CATALOG = {
        "DBMS": {"credits": 4, "prereq": "Programming", "slot": "MON_09:00", "capacity": 60},
        "AI": {"credits": 4, "prereq": "Data Structures", "slot": "TUE_10:00", "capacity": 40},
        "ML": {"credits": 3, "prereq": "Statistics", "slot": "MON_09:00", "capacity": 30},
        "Cloud": {"credits": 3, "prereq": "Networking", "slot": "WED_11:00", "capacity": 50}
    }

    def __init__(self, max_credits=20):
        self.max_credits = max_credits
        self.course_enrollments = {k: 0 for k in self.COURSE_CATALOG}

    def register_courses(self, student_id, program, semester, selected_courses, completed_courses):
        if not (1 <= semester <= 8):
            return {"status": "REJECTED", "reason": "Invalid semester restriction."}

        # Check duplicate selection
        if len(selected_courses) != len(set(selected_courses)):
            return {"status": "REJECTED", "reason": "Duplicate courses in selection."}

        total_credits = 0
        slots_occupied = {}

        for course in selected_courses:
            if course not in self.COURSE_CATALOG:
                return {"status": "REJECTED", "reason": f"Course {course} does not exist."}

            course_meta = self.COURSE_CATALOG[course]

            # Prerequisite Check
            prereq = course_meta["prereq"]
            if prereq and prereq not in completed_courses:
                return {"status": "REJECTED", "reason": f"Prerequisite {prereq} missing for {course}."}

            # Course Capacity
            if self.course_enrollments[course] >= course_meta["capacity"]:
                return {"status": "REJECTED", "reason": f"Course {course} is full."}

            # Timetable Conflict
            slot = course_meta["slot"]
            if slot in slots_occupied:
                return {"status": "REJECTED", "reason": f"Timetable conflict between {course} and {slots_occupied[slot]}."}
            slots_occupied[slot] = course

            total_credits += course_meta["credits"]

        # Credit limit validation
        if total_credits > self.max_credits:
            return {"status": "REJECTED", "reason": f"Credit limit exceeded. Attempted: {total_credits}, Max: {self.max_credits}"}

        # Finalize enrollments
        for c in selected_courses:
            self.course_enrollments[c] += 1

        return {
            "status": "APPROVED",
            "student_id": student_id,
            "registered_courses": selected_courses,
            "total_credits": total_credits
        }
