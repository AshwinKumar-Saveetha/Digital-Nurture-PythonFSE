import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  useNavigate,
  useParams,
} from "react-router-dom";

import { enroll } from "../redux/enrollmentSlice";
import { enrollStudent } from "../api/courseApi";

function CourseDetailPage({ courses }) {
  const { courseId } = useParams();

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [isEnrolling, setIsEnrolling] =
    useState(false);
  const [enrollmentError, setEnrollmentError] =
    useState("");

  const enrolledCourses = useSelector(
    (state) => state.enrollment.enrolledCourses,
  );

  const course = courses.find(
    (item) => item.id === Number(courseId),
  );

  async function handleEnroll() {
    if (!course || isEnrolling) {
      return;
    }

    const alreadyEnrolled = enrolledCourses.some(
      (item) => item.id === course.id,
    );

    if (alreadyEnrolled) {
      alert("Course already enrolled.");
      return;
    }

    try {
      setIsEnrolling(true);
      setEnrollmentError("");

      await enrollStudent(1, course.id);

      dispatch(enroll(course));
      navigate("/profile");
    } catch (apiError) {
      const statusMessage = apiError.statusCode
        ? ` Error code: ${apiError.statusCode}.`
        : "";

      setEnrollmentError(
        `Enrollment could not be completed.${statusMessage}`,
      );
    } finally {
      setIsEnrolling(false);
    }
  }

  if (!course) {
    return (
      <main className="container">
        <section className="course-detail">
          <h2>Course Not Found</h2>

          <p>
            No course exists with ID {courseId}.
          </p>

          <button
            type="button"
            className="details-btn"
            onClick={() => navigate("/courses")}
          >
            Back to Courses
          </button>
        </section>
      </main>
    );
  }

  return (
    <main className="container">
      <section
        className="course-detail"
        aria-labelledby="course-detail-heading"
      >
        <h2 id="course-detail-heading">
          {course.name}
        </h2>

        <p>
          <strong>Course ID:</strong> {course.id}
        </p>

        <p>
          <strong>Code:</strong> {course.code}
        </p>

        <p>
          <strong>Credits:</strong> {course.credits}
        </p>

        <p>
          <strong>Grade:</strong> {course.grade}
        </p>

        {course.description && (
          <p>
            <strong>Description:</strong>{" "}
            {course.description}
          </p>
        )}

        {enrollmentError && (
          <div
            className="api-error-message"
            role="alert"
          >
            <p>{enrollmentError}</p>
          </div>
        )}

        <div className="course-detail-actions">
          <button
            type="button"
            className="details-btn"
            onClick={() => navigate("/courses")}
          >
            Back to Courses
          </button>

          <button
            type="button"
            className="enroll-btn"
            onClick={handleEnroll}
            disabled={isEnrolling}
          >
            {isEnrolling
              ? "Enrolling..."
              : "Enroll"}
          </button>
        </div>
      </section>
    </main>
  );
}

export default CourseDetailPage;