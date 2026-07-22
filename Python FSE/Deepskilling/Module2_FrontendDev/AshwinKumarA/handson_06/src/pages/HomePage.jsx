import { Link } from "react-router-dom";

function HomePage() {
  return (
    <main className="container home-page">
      <h2>Welcome to the Student Portal</h2>

      <p>
        Browse available courses, view course details and manage your
        enrollment.
      </p>

      <Link className="explore-btn" to="/courses">
        Explore Courses
      </Link>
    </main>
  );
}

export default HomePage;