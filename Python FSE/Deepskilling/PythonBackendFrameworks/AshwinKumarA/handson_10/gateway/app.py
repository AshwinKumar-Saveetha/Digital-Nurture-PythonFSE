import requests
from flask import Flask, Response, jsonify, request


app = Flask(__name__)

COURSE_SERVICE_URL = "http://127.0.0.1:5001"
STUDENT_SERVICE_URL = "http://127.0.0.1:5002"


def forward_request(service_url: str, path: str) -> Response:
    target_url = f"{service_url}/{path}"

    forwarded_headers = {
        key: value
        for key, value in request.headers
        if key.lower()
        not in {
            "host",
            "content-length",
            "connection",
        }
    }

    try:
        service_response = requests.request(
            method=request.method,
            url=target_url,
            params=request.args,
            data=request.get_data(),
            headers=forwarded_headers,
            timeout=10,
            allow_redirects=False,
        )

    except requests.exceptions.ConnectionError:
        return jsonify(
            {
                "error": (
                    "The requested microservice is unavailable"
                ),
                "service_url": service_url,
            }
        ), 503

    except requests.exceptions.Timeout:
        return jsonify(
            {
                "error": (
                    "The requested microservice did not respond in time"
                ),
                "service_url": service_url,
            }
        ), 504

    excluded_response_headers = {
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    }

    response_headers = [
        (name, value)
        for name, value in service_response.headers.items()
        if name.lower() not in excluded_response_headers
    ]

    return Response(
        response=service_response.content,
        status=service_response.status_code,
        headers=response_headers,
        content_type=service_response.headers.get(
            "Content-Type",
            "application/json",
        ),
    )


@app.get("/")
def root():
    return jsonify(
        {
            "service": "API Gateway",
            "status": "running",
            "port": 5000,
            "routes": {
                "/api/courses/*": "Course Service",
                "/api/students/*": "Student Service",
            },
        }
    )


@app.route(
    "/api/courses/",
    defaults={"subpath": ""},
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
)
@app.route(
    "/api/courses/<path:subpath>",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
)
def course_gateway(subpath: str):
    path = "api/courses/"

    if subpath:
        path = f"{path}{subpath}"

    return forward_request(
        COURSE_SERVICE_URL,
        path,
    )


@app.route(
    "/api/students/",
    defaults={"subpath": ""},
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
)
@app.route(
    "/api/students/<path:subpath>",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
)
def student_gateway(subpath: str):
    path = "api/students/"

    if subpath:
        path = f"{path}{subpath}"

    return forward_request(
        STUDENT_SERVICE_URL,
        path,
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False,
    )