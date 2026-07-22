import { useEffect, useState } from "react";
import { Route, Routes } from "react-router-dom";

import Header from "./components/Header";
import Footer from "./components/Footer";

import HomePage from "./pages/HomePage";
import CoursesPage from "./pages/CoursesPage";
import CourseDetailPage from "./pages/CourseDetailPage";
import ProfilePage from "./pages/ProfilePage";

import { courses as courseData } from "./data/courses";

import "./App.css";

function App() {
  const [courses] = useState(courseData);

  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchPosts() {
      try {
        setLoading(true);

        const response = await fetch(
          "https://jsonplaceholder.typicode.com/posts"
        );

        if (!response.ok) {
          throw new Error("Failed to fetch notifications.");
        }

        const data = await response.json();
        setPosts(data.slice(0, 5));
      } catch (fetchError) {
        setError(fetchError.message);
      } finally {
        setLoading(false);
      }
    }

    fetchPosts();
  }, []);

  return (
    <>
      <Header siteName="Student Portal" />

      <Routes>
        <Route
          path="/"
          element={<HomePage />}
        />

        <Route
          path="/courses"
          element={
            <CoursesPage courses={courses} />
          }
        />

        <Route
          path="/courses/:courseId"
          element={
            <CourseDetailPage courses={courses} />
          }
        />

        <Route
          path="/profile"
          element={<ProfilePage />}
        />

        <Route
          path="*"
          element={
            <main className="container">
              <h2>Page Not Found</h2>
            </main>
          }
        />
      </Routes>

      <section className="notifications">
        <h2>Latest Notifications</h2>

        {loading && <p>Loading notifications...</p>}

        {error && <p className="error">{error}</p>}

        {!loading &&
          !error &&
          posts.map((post) => (
            <div
              key={post.id}
              className="notification-card"
            >
              <h3>{post.title}</h3>
              <p>{post.body}</p>
            </div>
          ))}
      </section>

      <Footer />
    </>
  );
}

export default App;