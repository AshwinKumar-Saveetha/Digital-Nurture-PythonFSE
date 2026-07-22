import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

import CourseCard from "../components/CourseCard";
import { enroll } from "../redux/enrollmentSlice";

function CoursesPage({ courses }) {
  const [search, setSearch] = useState("");

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const enrolledCourses = useSelector(
    (state) => state.enrollment.enrolledCourses
  );

  const filteredCourses = courses.filter((course) =>
    course.name
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  function viewCourseDetails(courseId) {
    navigate(`/courses/${courseId}`);
  }

  function handleEnroll(course) {
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

  return (
    <main className="container">
      <h2>Available Courses</h2>

      <input
        type="text"
        className="search-box"
        placeholder="Search Courses..."
        value={search}
        onChange={(event) =>
          setSearch(event.target.value)
        }
      />

      <div className="course-grid">
        {filteredCourses.map((course) => (
          <CourseCard
            key={course.id}
            {...course}
            onViewDetails={viewCourseDetails}
            onEnroll={() => handleEnroll(course)}
          />
        ))}
      </div>

      {filteredCourses.length === 0 && (
        <p className="error">
          No courses found.
        </p>
      )}
    </main>
  );
}

export default CoursesPage;