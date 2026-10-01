"""
Student Course Selection Optimizer Engine
DAA Hackathon Implementation: DAG Prerequisite Filtering + CSP Backtracking
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="CourseCraft Optimizer Engine")

# --- DATA MODELS ---
class TimeSlot(BaseModel):
    slot_id: str
    day: str
    start_time: int  # e.g., 900 for 09:00 AM
    end_time: int    # e.g., 1030 for 10:30 AM

class Course(BaseModel):
    id: str
    name: str
    credits: int
    prerequisites: List[str]
    difficulty: int
    slots: List[TimeSlot]

class OptimizationRequest(BaseModel):
    completed_courses: List[str]
    min_credits: int
    max_credits: int
    catalog: List[Course]

# --- DAA HELPER FUNCTIONS ---
def check_overlap(slot1: TimeSlot, slot2: TimeSlot) -> bool:
    """Checks if two time slots overlap on the same day."""
    if slot1.day != slot2.day:
        return False
    # Overlap occurs if max(starts) < min(ends)
    return max(slot1.start_time, slot2.start_time) < min(slot1.end_time, slot2.end_time)

def filter_eligible_courses(catalog: List[Course], completed: List[str]) -> List[Course]:
    """Phase 1: DAG Prerequisite Filter - O(V + E) complexity."""
    completed_set = set(completed)
    eligible = []
    for course in catalog:
        if course.id in completed_set:
            continue
        # Course is eligible only if ALL prerequisites are completed
        if all(prereq in completed_set for prereq in course.prerequisites):
            eligible.append(course)
    return eligible

# --- API ENDPOINT ---
@app.post("/api/optimize")
def optimize_schedule(req: OptimizationRequest):
    # Phase 1: Filter eligible courses based on DAG prerequisites
    eligible_courses = filter_eligible_courses(req.catalog, req.completed_courses)
    valid_schedules = []

    # Phase 2: Backtracking CSP Solver
    def backtrack(index: int, current_slots: List[TimeSlot], current_courses: List[str], current_credits: int):
        # Upper bound constraint
        if current_credits > req.max_credits:
            return
        
        # Valid solution condition
        if current_credits >= req.min_credits:
            valid_schedules.append({
                "courses": list(current_courses),
                "slots": [s.slot_id for s in current_slots],
                "total_credits": current_credits
            })

        if index >= len(eligible_courses):
            return

        course = eligible_courses[index]

        # Branch 1: Skip this course
        backtrack(index + 1, current_slots, current_courses, current_credits)

        # Branch 2: Try each available time slot section
        for slot in course.slots:
            has_conflict = any(check_overlap(slot, existing) for existing in current_slots)
            if not has_conflict:
                current_slots.append(slot)
                current_courses.append(course.id)
                
                # Recursive call
                backtrack(
                    index + 1,
                    current_slots,
                    current_courses,
                    current_credits + course.credits
                )
                
                # Backtrack step
                current_slots.pop()
                current_courses.pop()

    backtrack(0, [], [], 0)

    if not valid_schedules:
        return {
            "status": "NO_SOLUTION_FOUND",
            "message": "No valid schedule satisfies credit bounds without time conflicts."
        }

    return {
        "status": "SUCCESS",
        "eligible_count": len(eligible_courses),
        "total_valid_options": len(valid_schedules),
        "schedules": valid_schedules[:3]  # Return top 3 options
    }