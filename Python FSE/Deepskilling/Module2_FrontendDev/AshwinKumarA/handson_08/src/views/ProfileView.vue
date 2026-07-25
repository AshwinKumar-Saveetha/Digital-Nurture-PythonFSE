<template>
  <main class="profile-view">
    <section class="profile-container">
      <div class="profile-card">
        <div
          class="profile-icon"
          aria-hidden="true"
        >
          S
        </div>

        <h1>Student Profile</h1>

        <div class="profile-details">
          <p>
            <strong>Name:</strong>
            Ashwin Kumar A
          </p>

          <p>
            <strong>Email:</strong>
            ashwin@example.com
          </p>

          <p>
            <strong>Semester:</strong>
            6
          </p>
        </div>
      </div>

      <section class="enrollment-section">
        <div class="enrollment-heading">
          <div>
            <h2>Enrolled Courses</h2>

            <p>
              {{ store.enrolledCourses.length }}
              course(s) enrolled
            </p>
          </div>

          <div class="credits-summary">
            <span>Total Credits</span>
            <strong>{{ store.totalCredits }}</strong>
          </div>
        </div>

        <div
          v-if="store.enrolledCourses.length > 0"
          class="enrolled-list"
        >
          <article
            v-for="course in store.enrolledCourses"
            :key="course.id"
            class="enrolled-course"
          >
            <div class="course-information">
              <h3>{{ course.name }}</h3>

              <p>
                {{ course.code }} ·
                {{ course.credits }} credits
              </p>
            </div>

            <button
              class="unenroll-button"
              type="button"
              @click="store.unenroll(course.id)"
            >
              Unenroll
            </button>
          </article>
        </div>

        <div v-else class="empty-state">
          <h3>No Enrolled Courses</h3>

          <p>
            Select courses from the courses page to
            view them here.
          </p>

          <RouterLink
            class="courses-button"
            to="/courses"
          >
            Browse Courses
          </RouterLink>
        </div>
      </section>
    </section>
  </main>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useEnrollmentStore } from '../stores/enrollment'

const store = useEnrollmentStore()
</script>

<style scoped>
.profile-view {
  min-height: calc(100vh - 84px);
  padding: 40px 20px;
  background-color: #f4f6ee;
}

.profile-container {
  display: grid;
  grid-template-columns: minmax(280px, 0.8fr)
    minmax(400px, 1.4fr);
  gap: 24px;
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
}

.profile-card,
.enrollment-section {
  border: 1px solid #d8ddc5;
  border-radius: 14px;
  background-color: #ffffff;
  box-shadow: 0 8px 24px rgb(32 37 26 / 11%);
}

.profile-card {
  padding: 38px;
  text-align: center;
}

.profile-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 76px;
  height: 76px;
  margin: 0 auto 18px;
  border-radius: 50%;
  background-color: #bfd42f;
  color: #20251a;
  font-size: 2rem;
  font-weight: 700;
}

.profile-card h1 {
  margin-bottom: 25px;
  color: #20251a;
}

.profile-details {
  padding: 22px;
  border-radius: 9px;
  background-color: #f8faea;
  text-align: left;
}

.profile-details p {
  margin-bottom: 12px;
  color: #596048;
  line-height: 1.5;
}

.profile-details p:last-child {
  margin-bottom: 0;
}

.profile-details strong {
  color: #20251a;
}

.enrollment-section {
  padding: 30px;
}

.enrollment-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e0e5ce;
}

.enrollment-heading h2 {
  margin-bottom: 6px;
  color: #20251a;
}

.enrollment-heading p {
  color: #596048;
}

.credits-summary {
  min-width: 110px;
  padding: 13px 16px;
  border-radius: 9px;
  background-color: #eff5c7;
  text-align: center;
}

.credits-summary span {
  display: block;
  margin-bottom: 5px;
  color: #596048;
  font-size: 0.85rem;
}

.credits-summary strong {
  color: #4d5900;
  font-size: 1.5rem;
}

.enrolled-list {
  display: grid;
  gap: 14px;
}

.enrolled-course {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 18px;
  border: 1px solid #e0e5ce;
  border-left: 5px solid #bfd42f;
  border-radius: 8px;
  background-color: #fdfef8;
}

.course-information h3 {
  margin-bottom: 7px;
  color: #20251a;
  font-size: 1.05rem;
}

.course-information p {
  color: #596048;
  line-height: 1.4;
}

.unenroll-button {
  flex-shrink: 0;
  padding: 9px 14px;
  border: 1px solid #8b3a3a;
  border-radius: 6px;
  background-color: #ffffff;
  color: #8b3a3a;
  font-weight: 700;
  cursor: pointer;
}

.unenroll-button:hover {
  background-color: #8b3a3a;
  color: #ffffff;
}

.unenroll-button:focus {
  outline: 3px solid rgb(139 58 58 / 30%);
  outline-offset: 2px;
}

.empty-state {
  padding: 35px 20px;
  border-radius: 9px;
  background-color: #f8faea;
  text-align: center;
}

.empty-state h3 {
  margin-bottom: 10px;
  color: #20251a;
}

.empty-state p {
  max-width: 420px;
  margin: 0 auto 22px;
  color: #596048;
  line-height: 1.6;
}

.courses-button {
  display: inline-block;
  padding: 12px 20px;
  border-radius: 7px;
  background-color: #bfd42f;
  color: #20251a;
  font-weight: 700;
  text-decoration: none;
}

.courses-button:hover {
  background-color: #aabd20;
  color: #20251a;
}

.courses-button:focus {
  outline: 3px solid #718000;
  outline-offset: 3px;
}

@media (max-width: 800px) {
  .profile-container {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 520px) {
  .enrollment-heading {
    align-items: stretch;
    flex-direction: column;
  }

  .credits-summary {
    width: 100%;
  }

  .enrolled-course {
    align-items: stretch;
    flex-direction: column;
  }

  .unenroll-button {
    width: 100%;
  }
}
</style>