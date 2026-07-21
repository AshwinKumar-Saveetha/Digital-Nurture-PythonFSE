import { useState, useEffect } from "react";
import Header from "./components/Header";
import Footer from "./components/Footer";
import CourseCard from "./components/CourseCard";
import StudentProfile from "./components/StudentProfile";

import { courses as courseData } from "./data/courses";

import "./App.css";

function App() {

  const [courses] = useState(courseData);

  const [search, setSearch] = useState("");

  const [enrolledCourses, setEnrolledCourses] = useState([]);

  const [posts, setPosts] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  const filteredCourses = courses.filter((course) =>
    course.name.toLowerCase().includes(search.toLowerCase())
  );

  function enrollCourse(course) {

    const alreadyEnrolled =
      enrolledCourses.some(
        (item) => item.id === course.id
      );

    if (alreadyEnrolled) {
      alert("Course already enrolled.");
      return;
    }

    setEnrolledCourses([
      ...enrolledCourses,
      course
    ]);
  }
  useEffect(() => {

  async function fetchPosts() {

    try {

      setLoading(true);

      const response =
        await fetch(
          "https://jsonplaceholder.typicode.com/posts"
        );

      if (!response.ok) {

        throw new Error(
          "Failed to fetch notifications."
        );

      }

      const data =
        await response.json();

      setPosts(data.slice(0,5));

    }

    catch(error){

      setError(error.message);

    }

    finally{

      setLoading(false);

    }

  }

  fetchPosts();

}, []);

  return (
    <>
      <Header
        siteName="Student Portal"
        enrolledCount={enrolledCourses.length}
      />

      <main className="container">

        <h2>Available Courses</h2>

        <input
          type="text"
          className="search-box"
          placeholder="Search Courses..."
          value={search}
          onChange={(e) =>
            setSearch(e.target.value)
          }
        />

        <div className="course-grid">

          {filteredCourses.map((course) => (

            <CourseCard
              key={course.id}
              {...course}
              onEnroll={() =>
                enrollCourse(course)
              }
            />

          ))}

        </div>

      </main>
          <section className="notifications">

          <h2>Latest Notifications</h2>

          {loading &&

          <p>
          Loading notifications...
          </p>

          }
          {error &&

          <p className="error">

          {error}

          </p>

          }
          {

          !loading &&

          !error &&

          posts.map((post)=>(

          <div
          key={post.id}
          className="notification-card"
          >

          <h3>

          {post.title}

          </h3>

          <p>

          {post.body}

          </p>

          </div>

          ))

          }

          </section>
          <StudentProfile />
      <Footer />
    </>
  );
}

export default App;