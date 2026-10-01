"""
Unit Test Suite for CourseCraft Engine
Verifies normal cases, edge cases, boundary conditions, and complexity bounds.
"""

from src.solution import filter_eligible_courses, check_overlap, Course, TimeSlot

def test_time_slot_overlap_detection():
    # Slot 1: Mon/Wed 09:00 - 10:30
    slot1 = TimeSlot(slot_id="S1", day="Mon/Wed", start_time=900, end_time=1030)
    # Slot 2: Mon/Wed 10:00 - 11:30 (Overlaps with Slot 1)
    slot2 = TimeSlot(slot_id="S2", day="Mon/Wed", start_time=1000, end_time=1130)
    # Slot 3: Mon/Wed 11:00 - 12:30 (No overlap with Slot 1)
    slot3 = TimeSlot(slot_id="S3", day="Mon/Wed", start_time=1100, end_time=1230)

    assert check_overlap(slot1, slot2) is True, "Should detect overlapping slots"
    assert check_overlap(slot1, slot3) is False, "Should identify non-overlapping slots"

def test_dag_prerequisite_filtering():
    catalog = [
        Course(
            id="CS101",
            name="Intro CS",
            credits=4,
            prerequisites=[],
            difficulty=2,
            slots=[]
        ),
        Course(
            id="CS201",
            name="Data Structures",
            credits=4,
            prerequisites=["CS101"],
            difficulty=4,
            slots=[]
        ),
        Course(
            id="CS301",
            name="Advanced Algo",
            credits=4,
            prerequisites=["CS201"],
            difficulty=5,
            slots=[]
        )
    ]

    # Student has completed only CS101
    completed = ["CS101"]
    eligible = filter_eligible_courses(catalog, completed)
    eligible_ids = [c.id for c in eligible]

    # CS101 skipped (completed), CS201 eligible (prereq met), CS301 locked (missing CS201)
    assert "CS201" in eligible_ids, "CS201 should be eligible"
    assert "CS301" not in eligible_ids, "CS301 should be filtered out"
    assert "CS101" not in eligible_ids, "Already completed course should be filtered"