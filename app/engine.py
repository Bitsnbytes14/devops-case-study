"""Deterministic, explainable roommate allocation logic."""
from __future__ import annotations

from collections import defaultdict
from itertools import combinations
from math import sqrt

SOFT_FIELDS = ("sleep_schedule", "cleanliness", "noise_tolerance", "study_hours", "social_level")


def hard_constraint_check(first: dict, second: dict) -> tuple[bool, list[str]]:
    """Return whether two students can share a room and the rejection reasons."""
    reasons = []
    for field, label in (("gender", "gender"), ("smoking", "smoking preference"), ("alcohol", "alcohol preference"), ("room_size", "room size")):
        if first[field] != second[field]:
            reasons.append(f"{label} differs")
    return not reasons, reasons


def compatibility_score(first: dict, second: dict) -> float:
    """Calculate cosine similarity of soft preferences on a 0 to 100 scale."""
    valid, _ = hard_constraint_check(first, second)
    if not valid:
        return 0.0
    a = [float(first[key]) / 5 for key in SOFT_FIELDS]
    b = [float(second[key]) / 5 for key in SOFT_FIELDS]
    denominator = sqrt(sum(value * value for value in a)) * sqrt(sum(value * value for value in b))
    return round(100 * sum(x * y for x, y in zip(a, b)) / denominator, 2) if denominator else 0.0


def explanation(first: dict, second: dict) -> dict:
    deltas = sorted(((key, abs(first[key] - second[key])) for key in SOFT_FIELDS), key=lambda item: (item[1], item[0]))
    return {"top_matching_factors": [key for key, _ in deltas[:2]], "top_differing_factors": [key for key, _ in deltas[-2:][::-1]]}


def _room_score(members: list[dict]) -> float:
    scores = [compatibility_score(a, b) for a, b in combinations(members, 2)]
    return round(sum(scores) / len(scores), 2) if scores else 100.0


def _signal(score: float) -> str:
    return "GOOD" if score >= 80 else "REVIEW" if score >= 60 else "POOR"


def allocate(students: list[dict]) -> dict:
    """Greedily create valid rooms then improve them with deterministic swaps."""
    grouped = defaultdict(list)
    for student in sorted(students, key=lambda item: str(item["id"])):
        grouped[(student["gender"], student["room_size"], student["smoking"], student["alcohol"])].append(student)
    rooms, warnings, room_number = [], [], 1
    for key in sorted(grouped, key=str):
        members = grouped[key]
        size = key[1]
        while len(members) >= size:
            seed = members.pop(0)
            candidates = sorted(members, key=lambda candidate: (-compatibility_score(seed, candidate), str(candidate["id"])))
            chosen = candidates[: size - 1]
            for candidate in chosen:
                members.remove(candidate)
            room = [seed, *chosen]
            rooms.append({"room_id": f"R{room_number:03d}", "members": room})
            room_number += 1
        if members:
            warnings.append(f"{len(members)} student or students from group {key[0]} size {size} placed in a valid partial room")
            rooms.append({"room_id": f"R{room_number:03d}", "members": members})
            room_number += 1
    # Local search is only legal within equal hard constraint groups.
    for first, second in combinations(rooms, 2):
        if len(first["members"]) != len(second["members"]) or len(first["members"]) < 2:
            continue
        old = _room_score(first["members"]) + _room_score(second["members"])
        for i, left in enumerate(first["members"]):
            for j, right in enumerate(second["members"]):
                trial_a, trial_b = first["members"][:], second["members"][:]
                trial_a[i], trial_b[j] = right, left
                if all(hard_constraint_check(a, b)[0] for a, b in combinations(trial_a + trial_b, 2) if (a in trial_a and b in trial_a) or (a in trial_b and b in trial_b)):
                    if _room_score(trial_a) + _room_score(trial_b) > old:
                        first["members"], second["members"] = trial_a, trial_b
    result_rooms = []
    for room in rooms:
        members = room["members"]
        score = _room_score(members)
        pairs = [{"student_ids": [a["id"], b["id"]], "score": compatibility_score(a, b), "explanation": explanation(a, b)} for a, b in combinations(members, 2)]
        result_rooms.append({"room_id": room["room_id"], "student_ids": [item["id"] for item in members], "average_score": score, "signal": _signal(score), "pair_explanations": pairs})
    return {"rooms": result_rooms, "warnings": warnings, "students_allocated": len(students)}
