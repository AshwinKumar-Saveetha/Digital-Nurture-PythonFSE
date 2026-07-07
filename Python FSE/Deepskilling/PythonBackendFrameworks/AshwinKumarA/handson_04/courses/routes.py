from flask import Blueprint, jsonify, request, abort

courses_bp = Blueprint(
    "courses",
    __name__,
    url_prefix="/api/courses"
)

courses = []
next_course_id = 1


def make_response_json(data, status_code=200):
    response = {
        "status": "success",
        "data": data
    }
    return jsonify(response), status_code


def find_course(course_id):
    for course in courses:
        if course["id"] == course_id:
            return course
    return None


@courses_bp.route("/", methods=["GET"])
def get_courses():
    return jsonify(courses)


@courses_bp.route("/", methods=["POST"])
def create_course():
    global next_course_id

    data = request.get_json()

    if data is None:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    required_fields = ["name", "code", "credits"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400

    course = {
        "id": next_course_id,
        "name": data["name"],
        "code": data["code"],
        "credits": data["credits"]
    }

    courses.append(course)
    next_course_id += 1

    return make_response_json(course, 201)


@courses_bp.route("/<int:course_id>/", methods=["GET"])
def get_course(course_id):
    course = find_course(course_id)

    if course is None:
        abort(404)

    return make_response_json(course, 200)


@courses_bp.route("/<int:course_id>/", methods=["PUT"])
def update_course(course_id):
    course = find_course(course_id)

    if course is None:
        abort(404)

    data = request.get_json()

    if data is None:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    required_fields = ["name", "code", "credits"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400

    course["name"] = data["name"]
    course["code"] = data["code"]
    course["credits"] = data["credits"]

    return make_response_json(course, 200)


@courses_bp.route("/<int:course_id>/", methods=["DELETE"])
def delete_course(course_id):
    course = find_course(course_id)

    if course is None:
        abort(404)

    courses.remove(course)

    return make_response_json({"message": "Course deleted successfully"}, 200)