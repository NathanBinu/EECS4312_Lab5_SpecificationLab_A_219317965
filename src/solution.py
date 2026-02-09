## Student Name: Nathan Binu Edappilly
## Student ID: 219317965

from typing import List, Dict, Tuple

from datetime import datetime

WORK_START = "09:00"
WORK_END = "17:00"
LUNCH_START = "12:00"
LUNCH_END = "13:00"
SLOT_STEP_MIN = 15

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""
from typing import List, Dict

def _is_friday(day: str) -> bool:
    # Accepting both day abbreviations and YYYY-MM-DD dates
    if not day:
        return False
    d = day.strip()
    if d.lower() in {"fri", "friday"}:
        return True
    # Try YYYY-MM-DD
    try:
        return datetime.strptime(d, "%Y-%m-%d").weekday() == 4  # Monday=0 ... Friday=4
    except ValueError:
        return False

def _to_minutes(hhmm: str) -> int:
    hh, mm = hhmm.split(":")
    return int(hh) * 60 + int(mm)


def _to_hhmm(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def _overlaps(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
    return a_start < b_end and a_end > b_start


def _ceil_to_step(t: int, step: int) -> int:
    #Rounding up minutes upto the next multiple of step.
    return ((t + step - 1) // step) * step

def suggest_slots(
    events: List[Dict[str, str]],
    meeting_duration: int,
    day: str
) -> List[str]:
    if meeting_duration <= 0:
        return []

    work_start = _to_minutes(WORK_START)
    work_end = _to_minutes(WORK_END)
    lunch_start = _to_minutes(LUNCH_START)
    lunch_end = _to_minutes(LUNCH_END)

    normalized: List[Tuple[int, int]] = []
    for e in events:
        s = _to_minutes(e["start"])
        en = _to_minutes(e["end"])
        if en <= s:
            continue
        s = max(s, work_start)
        en = min(en, work_end)
        if en > s:
            normalized.append((s, en))

    latest_start = work_end - meeting_duration
    if latest_start < work_start:
        return []
    
    if _is_friday(day):
        friday_cutoff = _to_minutes("15:00")
        latest_start = min(latest_start, friday_cutoff)
        if latest_start < work_start:
            return []

    slots: List[str] = []

    t = work_start
    t = _ceil_to_step(t, SLOT_STEP_MIN)

    while t <= latest_start:
        # Lunch rule: cannot start a meeting during lunch
        if lunch_start <= t < lunch_end:
            t = _ceil_to_step(lunch_end, SLOT_STEP_MIN)
            continue

        meeting_end = t + meeting_duration
        if meeting_end > work_end:
            break

        # If conflict then jump t to next step boundary after the conflicting event ends
        jumped = False
        for es, ee in normalized:
            if _overlaps(t, meeting_end, es, ee):
                t = _ceil_to_step(ee + 1, SLOT_STEP_MIN)  # +1 makes sure that we move past boundary
                jumped = True
                break

        if jumped:
            continue

        slots.append(_to_hhmm(t))
        t += SLOT_STEP_MIN


    return slots
    """
    Suggest possible meeting start times for a given day.

    Args:
        events: List of dicts with keys {"start": "HH:MM", "end": "HH:MM"}
        meeting_duration: Desired meeting length in minutes
        day: Three-letter day abbreviation (e.g., "Mon", "Tue", ... "Fri")

    Returns:
        List of valid start times as "HH:MM" sorted ascending
    """
    # TODO: Implement this function
    #raise NotImplementedError("suggest_slots function has not been implemented yet")