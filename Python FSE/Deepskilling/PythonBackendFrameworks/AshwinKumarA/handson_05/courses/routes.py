from flask import Blueprint, request

from app import db
from courses.models import Course, Enrollment, Student


courses_bp = Blueprint("courses", __name__, url_prefix="/api/courses")


def make_response_json(data, status_code=200):
    return {
        "status": "success",
        "data": data
    }, status_code


@courses_bp.route("/", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    return make_response_json([course.to_dict() for course in courses], 200)


@courses_bp.route("/", methods=["POST"])
def create_course():
    data = request.get_json()

    if data is None:
        return {
            "status": "error",
            "message": "Request body must be JSON"
        }, 400

    required_fields = ["name", "code", "credits", "department_id"]
    missing_fields = [
        field for field in required_fields
        if field not in data or data[field] in [None, ""]
    ]

    if missing_fields:
        return {
            "status": "error",
            "message": "Missing required fields",
            "fields": missing_fields
        }, 400

    course = Course(
        name=data["name"],
        code=data["code"],
        credits=data["credits"],
        department_id=data["department_id"]
    )

    db.session.add(course)
    db.session.commit()

    return make_response_json(course.to_dict(), 201)


@courses_bp.route("/<int:id>/", methods=["GET"])
def get_course(id):
    course = Course.query.get_or_404(id)
    return make_response_json(course.to_dict(), 200)


@courses_bp.route("/<int:id>/", methods=["PUT"])
def update_course(id):
    course = Course.query.get_or_404(id)
    data = request.get_json()

    if data is None:
        return {
            "status": "error",
            "message": "Request body must be JSON"
        }, 400

    required_fields = ["name", "code", "credits", "department_id"]
    missing_fields = [
        field for field in required_fields
        if field not in data or data[field] in [None, ""]
    ]

    if missing_fields:
        return {
            "status": "error",
            "message": "Missing required fields",
            "fields": missing_fields
        }, 400

    course.name = data["name"]
    course.code = data["code"]
    course.credits = data["credits"]
    course.department_id = data["department_id"]

    db.session.commit()

    return make_response_json(course.to_dict(), 200)


@courses_bp.route("/<int:id>/", methods=["DELETE"])
def delete_course(id):
    course = Course.query.get_or_404(id)

    db.session.delete(course)
    db.session.commit()

    return make_response_json({"message": "Course deleted successfully"}, 200)


@courses_bp.route("/<int:id>/students/", methods=["GET"])
def get_course_students(id):
    Course.query.get_or_404(id)

    students = (
        Student.query
        .join(Enrollment, Student.id == Enrollment.student_id)
        .filter(Enrollment.course_id == id)
        .all()
    )

    return make_response_json([student.to_dict() for student in students], 200)