"""RoomFit Flask API."""
from __future__ import annotations
import os, random, time
from flask import Flask, jsonify, request
from prometheus_client import Counter, Gauge
from prometheus_flask_exporter import PrometheusMetrics
from app.engine import allocate, compatibility_score, hard_constraint_check

VERSION = os.getenv("APP_VERSION", "dev")
START = time.time()
app = Flask(__name__)
metrics = PrometheusMetrics(app, path="/metrics")
APP_INFO = Gauge("app_info", "RoomFit build information", ["version"]); APP_INFO.labels(VERSION).set(1)
APP_START = Gauge("app_start_time_seconds", "Service start timestamp"); APP_START.set(START)
ALLOCATIONS = Counter("allocations_total", "Allocation requests", ["status"])
STUDENTS = Counter("students_allocated_total", "Students allocated")
VIOLATIONS = Counter("hard_constraint_violations_total", "Hard constraint violations")
REQUIRED = {"id", "gender", "sleep_schedule", "cleanliness", "noise_tolerance", "study_hours", "social_level", "smoking", "alcohol", "room_size"}

def validate_student(student):
    missing = REQUIRED - set(student)
    if missing: raise ValueError("missing fields: " + ", ".join(sorted(missing)))
    if student["gender"] not in {"female", "male", "other"}: raise ValueError("gender must be female, male or other")
    if student["room_size"] not in {2, 3, 4}: raise ValueError("room_size must be 2, 3 or 4")
    if any(not isinstance(student[key], int) or not 1 <= student[key] <= 5 for key in ("sleep_schedule", "cleanliness", "noise_tolerance", "study_hours", "social_level")): raise ValueError("soft preferences must be integers from 1 to 5")
    if not all(isinstance(student[key], bool) for key in ("smoking", "alcohol")): raise ValueError("smoking and alcohol must be boolean")

@app.before_request
def chaos():
    if request.path.startswith("/api/"):
        time.sleep(max(0, int(os.getenv("EXTRA_LATENCY_MS", "0"))) / 1000)
        if random.random() < float(os.getenv("FAULT_RATE", "0")):
            return jsonify(error="injected fault"), 500

@app.errorhandler(ValueError)
def bad_request(error): return jsonify(error=str(error)), 400

@app.get("/")
def index(): return jsonify(service="roomfit-allocation-service", version=VERSION)
@app.get("/health")
def health(): return jsonify(status="ok", version=VERSION)
@app.get("/ready")
def ready(): return jsonify(status="ready")
@app.post("/api/v1/compatibility")
def compatibility():
    body = request.get_json(force=True); validate_student(body["first"]); validate_student(body["second"])
    valid, reasons = hard_constraint_check(body["first"], body["second"])
    if not valid: VIOLATIONS.inc()
    return jsonify(score=compatibility_score(body["first"], body["second"]), valid=valid, reasons=reasons)
@app.post("/api/v1/validate")
def validate():
    body = request.get_json(force=True); students = body.get("students", [])
    if len(students) < 2: raise ValueError("at least two students are required")
    for student in students: validate_student(student)
    valid, reasons = hard_constraint_check(students[0], students[1])
    if not valid: VIOLATIONS.inc()
    return jsonify(valid=valid, reasons=reasons)
@app.post("/api/v1/allocate")
def allocation():
    students = request.get_json(force=True).get("students", [])
    if not students: raise ValueError("students is required")
    for student in students: validate_student(student)
    result = allocate(students); ALLOCATIONS.labels("success").inc(); STUDENTS.inc(len(students)); return jsonify(result)
@app.get("/api/v1/sample")
def sample():
    students = [{"id": f"s{i}", "gender": "female" if i < 6 else "male", "sleep_schedule": 3 + i % 2, "cleanliness": 4, "noise_tolerance": 2 + i % 3, "study_hours": 3, "social_level": 3, "smoking": False, "alcohol": False, "room_size": 2} for i in range(12)]
    result = allocate(students); ALLOCATIONS.labels("success").inc(); STUDENTS.inc(12); return jsonify(result)

if __name__ == "__main__": app.run(host="0.0.0.0", port=5000)
