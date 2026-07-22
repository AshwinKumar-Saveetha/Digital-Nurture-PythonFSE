import { useDispatch, useSelector } from "react-redux";
import {
  useNavigate,
  useParams
} from "react-router-dom";

import { enroll } from "../redux/enrollmentSlice";

function CourseDetailPage({ courses }) {
  const { courseId } = useParams();

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const enrolledCourses = useSelector(
    (state) => state.enrollment.enrolledCourses
  );

  const course = courses.find(
    (item) => item.id === Number(courseId)
  );

  function handleEnroll() {
    if (!course) {
      return;
    }

    const alreadyEnrolled = enrolledCourses.some(
      (item) => item.id === course.id
    );

    if (alreadyEnrolled) {
      alert("Course already enrolled.");
      return;
    }

    dispatch(enroll(course));
    navigate("/profile");
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
            className="details-btn"
            onClick={() =>
              navigate("/courses")
            }
          >
            Back to Courses
          </button>
        </section>
      </main>
    );
  }

  return (
    <main className="container">
      <section className="course-detail">
        <h2>{course.name}</h2>

        <p>
          <strong>Course ID:</strong>{" "}
          {course.id}
        </p>

        <p>
          <strong>Code:</strong>{" "}
          {course.code}
        </p>

        <p>
          <strong>Credits:</strong>{" "}
          {course.credits}
        </p>

        <p>
          <strong>Grade:</strong>{" "}
          {course.grade}
        </p>

        <button
          className="details-btn"
          onClick={() =>
            navigate("/courses")
          }
        >
          Back to Courses
        </button>

        <button
          className="enroll-btn"
          onClick={handleEnroll}
        >
          Enroll
        </button>
      </section>
    </main>
  );
}

export default CourseDetailPage;