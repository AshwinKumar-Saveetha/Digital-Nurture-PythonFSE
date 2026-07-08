from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from courses.models import Course, Department, Enrollment, Student
    from courses.routes import courses_bp

    app.register_blueprint(courses_bp)

    Migrate(app, db)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)