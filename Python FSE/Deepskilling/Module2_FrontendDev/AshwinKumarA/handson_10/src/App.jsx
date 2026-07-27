import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { Route, Routes } from "react-router-dom";

import Header from "./components/Header";
import Footer from "./components/Footer";

import HomePage from "./pages/HomePage";
import CoursesPage from "./pages/CoursesPage";
import CourseDetailPage from "./pages/CourseDetailPage";
import ProfilePage from "./pages/ProfilePage";

import { selectCourses } from "./redux/courseSlice";
import { getLatestNotifications } from "./api/notificationApi";

import "./App.css";

function App() {
  const courses = useSelector(selectCourses);

  const [notifications, setNotifications] = useState([]);
  const [notificationsLoading, setNotificationsLoading] =
    useState(true);
  const [notificationsError, setNotificationsError] =
    useState("");

  useEffect(() => {
    async function loadNotifications() {
      try {
        setNotificationsLoading(true);
        setNotificationsError("");

        const latestNotifications =
          await getLatestNotifications(5);

        setNotifications(latestNotifications);
      } catch (apiError) {
        const statusMessage = apiError.statusCode
          ? ` Error code: ${apiError.statusCode}.`
          : "";

        setNotificationsError(
          `Unable to load notifications.${statusMessage}`,
        );
      } finally {
        setNotificationsLoading(false);
      }
    }

    loadNotifications();
  }, []);

  return (
    <>
      <Header siteName="Student Portal" />

      <Routes>
        <Route path="/" element={<HomePage />} />

        <Route
          path="/courses"
          element={<CoursesPage />}
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
              <section className="api-status-panel">
                <h2>Page Not Found</h2>

                <p>
                  The page you requested does not exist.
                </p>
              </section>
            </main>
          }
        />
      </Routes>

      <section
        className="notifications"
        aria-labelledby="notifications-heading"
      >
        <h2 id="notifications-heading">
          Latest Notifications
        </h2>

        {notificationsLoading && (
          <div
            className="api-loading-message"
            role="status"
            aria-live="polite"
          >
            <span
              className="api-loading-indicator"
              aria-hidden="true"
            />

            <p>Loading notifications...</p>
          </div>
        )}

        {notificationsError && (
          <div
            className="api-error-message"
            role="alert"
          >
            <p>{notificationsError}</p>
          </div>
        )}

        {!notificationsLoading &&
          !notificationsError &&
          notifications.map((notification) => (
            <article
              key={notification.id}
              className="notification-card"
            >
              <h3>{notification.title}</h3>
              <p>{notification.message}</p>
            </article>
          ))}
      </section>

      <Footer />
    </>
  );
}

export default App;