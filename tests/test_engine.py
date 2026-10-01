from app.engine import allocate, compatibility_score, hard_constraint_check

def student(ident, **changes):
    base = {"id": ident, "gender": "female", "sleep_schedule": 3, "cleanliness": 4, "noise_tolerance": 3, "study_hours": 4, "social_level": 3, "smoking": False, "alcohol": False, "room_size": 2}; base.update(changes); return base
def test_hard_constraints_and_zero_score():
    assert not hard_constraint_check(student("a"), student("b", smoking=True))[0]
    assert compatibility_score(student("a"), student("b", smoking=True)) == 0
def test_every_student_is_allocated_without_invalid_pair():
    result = allocate([student(str(i)) for i in range(5)])
    assert sorted(item for room in result["rooms"] for item in room["student_ids"]) == ["0", "1", "2", "3", "4"]
    assert result["warnings"]
def test_score_and_signal():
    result = allocate([student("a"), student("b")]); assert result["rooms"][0]["signal"] == "GOOD"
