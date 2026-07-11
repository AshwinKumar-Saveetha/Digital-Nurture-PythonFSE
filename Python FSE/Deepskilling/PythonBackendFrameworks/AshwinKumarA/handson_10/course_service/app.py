import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request


app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "course_service.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialise_database() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT NOT NULL UNIQUE,
                credits INTEGER NOT NULL,
                department_id INTEGER NOT NULL,
                FOREIGN KEY (department_id) REFERENCES departments(id)
            )
            """
        )

        department_count = connection.execute(
            "SELECT COUNT(*) AS count FROM departments"
        ).fetchone()["count"]

        if department_count == 0:
            connection.execute(
                "INSERT INTO departments (name) VALUES (?)",
                ("Computer Science",),
            )
            connection.execute(
                "INSERT INTO departments (name) VALUES (?)",
                ("Commerce",),
            )

        course_count = connection.execute(
            "SELECT COUNT(*) AS count FROM courses"
        ).fetchone()["count"]

        if course_count == 0:
            connection.execute(
                """
                INSERT INTO courses (name, code, credits, department_id)
                VALUES (?, ?, ?, ?)
                """,
                ("Python Programming", "CS101", 4, 1),
            )
            connection.execute(
                """
                INSERT INTO courses (name, code, credits, department_id)
                VALUES (?, ?, ?, ?)
                """,
                ("Database Systems", "CS102", 3, 1),
            )

        connection.commit()


@app.get("/")
def root():
    return jsonify(
        {
            "service": "Course Service",
            "status": "running",
            "port": 5001,
        }
    )


@app.get("/api/courses/")
def get_courses():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                courses.id,
                courses.name,
                courses.code,
                courses.credits,
                courses.department_id,
                departments.name AS department_name
            FROM courses
            JOIN departments
                ON departments.id = courses.department_id
            ORDER BY courses.id
            """
        ).fetchall()

    return jsonify([dict(row) for row in rows]), 200


@app.post("/api/courses/")
def create_course():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {
                "error": "Request body must contain valid JSON"
            }
        ), 400

    required_fields = [
        "name",
        "code",
        "credits",
        "department_id",
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
        department = connection.execute(
            "SELECT id FROM departments WHERE id = ?",
            (data["department_id"],),
        ).fetchone()

        if department is None:
            return jsonify(
                {
                    "error": "Department not found"
                }
            ), 404

        try:
            cursor = connection.execute(
                """
                INSERT INTO courses (
                    name,
                    code,
                    credits,
                    department_id
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    data["name"],
                    data["code"],
                    data["credits"],
                    data["department_id"],
                ),
            )
            connection.commit()

        except sqlite3.IntegrityError:
            return jsonify(
                {
                    "error": "Course code already exists"
                }
            ), 409

        course_id = cursor.lastrowid

        row = connection.execute(
            """
            SELECT
                id,
                name,
                code,
                credits,
                department_id
            FROM courses
            WHERE id = ?
            """,
            (course_id,),
        ).fetchone()

    response = jsonify(dict(row))
    response.status_code = 201
    response.headers["Location"] = f"/api/courses/{course_id}/"
    return response


@app.get("/api/courses/<int:course_id>/")
def get_course(course_id: int):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                courses.id,
                courses.name,
                courses.code,
                courses.credits,
                courses.department_id,
                departments.name AS department_name
            FROM courses
            JOIN departments
                ON departments.id = courses.department_id
            WHERE courses.id = ?
            """,
            (course_id,),
        ).fetchone()

    if row is None:
        return jsonify(
            {
                "error": f"Course with id {course_id} was not found"
            }
        ), 404

    return jsonify(dict(row)), 200


if __name__ == "__main__":
    initialise_database()
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True,
        use_reloader=False,
    )