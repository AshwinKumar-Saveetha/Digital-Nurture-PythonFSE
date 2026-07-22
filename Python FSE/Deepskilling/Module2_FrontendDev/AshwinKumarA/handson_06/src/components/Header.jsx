import { Link } from "react-router-dom";
import { useSelector } from "react-redux";

function Header({ siteName }) {
  const enrolledCourses = useSelector(
    (state) => state.enrollment.enrolledCourses
  );

  return (
    <header className="header">
      <h1>{siteName}</h1>

      <nav className="navigation">
        <Link to="/">Home</Link>
        <Link to="/courses">Courses</Link>
        <Link to="/profile">Profile</Link>
      </nav>

      <p className="enrolled-count">
        Enrolled Courses: {enrolledCourses.length}
      </p>
    </header>
  );
}

export default Header;