import {
  useEffect,
  useState,
} from "react";

import {
  useDispatch,
  useSelector,
} from "react-redux";

import { useNavigate } from "react-router-dom";

import CourseCard from "../components/CourseCard";

import { enroll } from "../redux/enrollmentSlice";

import {
  fetchAllCourses,
  selectCourses,
  selectCoursesError,
  selectCoursesLoading,
} from "../redux/courseSlice";

import { enrollStudent } from "../api/courseApi";

function CoursesPage() {
  const [search, setSearch] = useState("");
  const [enrollmentError, setEnrollmentError] =
    useState("");

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const courses = useSelector(selectCourses);

  const loading = useSelector(
    selectCoursesLoading,
  );

  const error = useSelector(
    selectCoursesError,
  );

  const enrolledCourses = useSelector(
    (state) => state.enrollment.enrolledCourses,
  );

  useEffect(() => {
    dispatch(fetchAllCourses());
  }, [dispatch]);

  const filteredCourses = courses.filter((course) =>
    course.name
      .toLowerCase()
      .includes(search.toLowerCase()),
  );

  function viewCourseDetails(courseId) {
    navigate(`/courses/${courseId}`);
  }

  async function handleEnroll(course) {
    const alreadyEnrolled = enrolledCourses.some(
      (item) => item.id === course.id,
    );

    if (alreadyEnrolled) {
      alert("Course already enrolled.");
      return;
    }

    try {
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
    }
  }

  return (
    <main className="container">
      <section
        aria-labelledby="available-courses-heading"
      >
        <h2 id="available-courses-heading">
          Available Courses
        </h2>

        <div className="search-field">
          <label htmlFor="course-search">
            Search courses
          </label>

          <input
            id="course-search"
            type="search"
            className="search-box"
            placeholder="Search Courses..."
            value={search}
            onChange={(event) =>
              setSearch(event.target.value)
            }
          />
        </div>

        {loading && (
          <div
            className="api-loading-message"
            role="status"
            aria-live="polite"
          >
            <span
              className="api-loading-indicator"
              aria-hidden="true"
            />

            <p>Loading courses...</p>
          </div>
        )}

        {error && !loading && (
          <div
            className="api-error-message"
            role="alert"
          >
            <p>{error}</p>

            <button
              type="button"
              className="primary-button"
              onClick={() =>
                dispatch(fetchAllCourses())
              }
            >
              Try Again
            </button>
          </div>
        )}

        {enrollmentError && (
          <div
            className="api-error-message"
            role="alert"
          >
            <p>{enrollmentError}</p>
          </div>
        )}

        {!loading && !error && (
          <>
            <p
              className="course-results-count"
              role="status"
              aria-live="polite"
            >
              {filteredCourses.length}{" "}
              {filteredCourses.length === 1
                ? "course"
                : "courses"}{" "}
              found
            </p>

            <div className="course-grid">
              {filteredCourses.map((course) => (
                <CourseCard
                  key={course.id}
                  {...course}
                  onViewDetails={viewCourseDetails}
                  onEnroll={() =>
                    handleEnroll(course)
                  }
                />
              ))}
            </div>

            {filteredCourses.length === 0 && (
              <p className="error">
                No courses found.
              </p>
            )}
          </>
        )}
      </section>
    </main>
  );
}

export default CoursesPage;