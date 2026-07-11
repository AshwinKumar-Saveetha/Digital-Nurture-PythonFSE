import sqlite3
from pathlib import Path

import requests
from flask import Flask, jsonify, request


app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "student_service.db"

COURSE_SERVICE_URL = "http://127.0.0.1:5001"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialise_database() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                UNIQUE(student_id, course_id),
                FOREIGN KEY (student_id) REFERENCES students(id)
            )
            """
        )

        student_count = connection.execute(
            "SELECT COUNT(*) AS count FROM students"
        ).fetchone()["count"]

        if student_count == 0:
            connection.execute(
                """
                INSERT INTO students (
                    first_name,
                    last_name,
                    email
                )
                VALUES (?, ?, ?)
                """,
                (
                    "Ashwin",
                    "Kumar",
                    "ashwin.student@example.com",
                ),
            )

        connection.commit()


@app.get("/")
def root():
    return jsonify(
        {
            "service": "Student Service",
            "status": "running",
            "port": 5002,
        }
    )


@app.get("/api/students/")
def get_students():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, first_name, last_name, email
            FROM students
            ORDER BY id
            """
        ).fetchall()

    return jsonify([dict(row) for row in rows]), 200


@app.post("/api/students/")
def create_student():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {
                "error": "Request body must contain valid JSON"
            }
        ), 400

    required_fields = [
        "first_name",
        "last_name",
        "email",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify(
            {
                "error": "Required fields are missing",
                "fields": missing_fields,
            }
        ), 400

    with get_connection() as connection:
        try:
            cursor = connection.execute(
                """
                INSERT INTO students (
                    first_name,
                    last_name,
                    email
                )
                VALUES (?, ?, ?)
                """,
                (
                    data["first_name"],
                    data["last_name"],
                    data["email"],
                ),
            )
            connection.commit()

        except sqlite3.IntegrityError:
            return jsonify(
                {
                    "error": "Student email already exists"
                }
            ), 409

        student_id = cursor.lastrowid

        row = connection.execute(
            """
            SELECT id, first_name, last_name, email
            FROM students
            WHERE id = ?
            """,
            (student_id,),
        ).fetchone()

    response = jsonify(dict(row))
    response.status_code = 201
    response.headers["Location"] = f"/api/students/{student_id}/"
    return response


@app.get("/api/students/<int:student_id>/")
def get_student(student_id: int):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, first_name, last_name, email
            FROM students
            WHERE id = ?
            """,
            (student_id,),
        ).fetchone()

    if row is None:
        return jsonify(
            {
                "error": f"Student with id {student_id} was not found"
            }
        ), 404

    return jsonify(dict(row)), 200


@app.get("/api/students/<int:student_id>/enrollments/")
def get_student_enrollments(student_id: int):
    with get_connection() as connection:
        student = connection.execute(
            "SELECT id FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()

        if student is None:
            return jsonify(
                {
                    "error": f"Student with id {student_id} was not found"
                }
            ), 404

        rows = connection.execute(
            """
            SELECT id, student_id, course_id
            FROM enrollments
            WHERE student_id = ?
            ORDER BY id
            """,
            (student_id,),
        ).fetchall()

    return jsonify([dict(row) for row in rows]), 200


@app.post("/api/students/<int:student_id>/enroll")
def enroll_student(student_id: int):
    data = request.get_json(silent=True)

    if data is None or "course_id" not in data:
        return jsonify(
            {
                "error": "course_id is required"
            }
        ), 400

    course_id = data["course_id"]

    with get_connection() as connection:
        student = connection.execute(
            """
            SELECT id, first_name, last_name, email
            FROM students
            WHERE id = ?
            """,
            (student_id,),
        ).fetchone()

    if student is None:
        return jsonify(
            {
                "error": f"Student with id {student_id} was not found"
            }
        ), 404

    try:
        course_response = requests.get(
            f"{COURSE_SERVICE_URL}/api/courses/{course_id}/",
            timeout=5,
        )

    except requests.exceptions.ConnectionError:
        return jsonify(
            {
                "error": (
                    "Course Service is unavailable. "
                    "Enrollment cannot be completed."
                )
            }
        ), 503

    except requests.exceptions.Timeout:
        return jsonify(
            {
                "error": (
                    "Course Service did not respond in time. "
                    "Enrollment cannot be completed."
                )
            }
        ), 503

    if course_response.status_code == 404:
        return jsonify(
            {
                "error": f"Course with id {course_id} was not found"
            }
        ), 404

    if not course_response.ok:
        return jsonify(
            {
                "error": (
                    "Course Service returned an unexpected response"
                ),
                "course_service_status": course_response.status_code,
            }
        ), 502

    course = course_response.json()

    with get_connection() as connection:
        try:
            cursor = connection.execute(
                """
                INSERT INTO enrollments (
                    student_id,
                    course_id
                )
                VALUES (?, ?)
                """,
                (student_id, course_id),
            )
            connection.commit()

        except sqlite3.IntegrityError:
            return jsonify(
                {
                    "error": (
                        "The student is already enrolled "
                        "in this course"
                    )
                }
            ), 409

        enrollment_id = cursor.lastrowid

    return jsonify(
        {
            "id": enrollment_id,
            "student": dict(student),
            "course": course,
            "message": "Student enrolled successfully",
        }
    ), 201


if __name__ == "__main__":
    initialise_database()
    app.run(
        host="127.0.0.1",
        port=5002,
        debug=True,
        use_reloader=False,
    )