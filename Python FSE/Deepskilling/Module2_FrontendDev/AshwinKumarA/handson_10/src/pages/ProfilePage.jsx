import {
  useDispatch,
  useSelector
} from "react-redux";

import StudentProfile from "../components/StudentProfile";
import { unenroll } from "../redux/enrollmentSlice";

function ProfilePage() {
  const dispatch = useDispatch();

  const enrolledCourses = useSelector(
    (state) => state.enrollment.enrolledCourses
  );

  function removeCourse(courseId) {
    dispatch(unenroll(courseId));
  }

  return (
    <main>
      <StudentProfile />

      <section className="student-profile">
        <h2>Enrolled Courses</h2>

        {enrolledCourses.length === 0 ? (
          <p>No courses enrolled yet.</p>
        ) : (
          <div className="enrolled-list">
            {enrolledCourses.map((course) => (
              <div
                className="enrolled-course"
                key={course.id}
              >
                <h3>{course.name}</h3>

                <p>
                  <strong>Code:</strong>{" "}
                  {course.code}
                </p>

                <p>
                  <strong>Credits:</strong>{" "}
                  {course.credits}
                </p>

                <button
                  type="button"
                  className="remove-btn"
                  onClick={() =>
                    removeCourse(course.id)
                  }
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}

export default ProfilePage;