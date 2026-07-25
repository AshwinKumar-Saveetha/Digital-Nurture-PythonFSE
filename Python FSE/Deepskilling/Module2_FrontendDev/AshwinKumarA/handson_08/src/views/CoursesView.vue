<template>
  <main class="courses-view">
    <section class="courses-section">
      <h1>My Courses</h1>

      <div class="search-container">
        <label for="search-courses">
          Search Courses
        </label>

        <input
          id="search-courses"
          v-model="searchTerm"
          type="text"
          placeholder="Search by course name"
        />
      </div>

      <div
        v-if="filteredCourses.length > 0"
        class="course-grid"
      >
        <div
          v-for="course in filteredCourses"
          :key="course.id"
          class="course-item"
        >
          <CourseCard
            :name="course.name"
            :code="course.code"
            :credits="course.credits"
            :grade="course.grade"
          />

          <div class="course-actions">
            <RouterLink
              class="details-button"
              :to="`/courses/${course.id}`"
            >
              View Details
            </RouterLink>

            <button
              class="enroll-button"
              type="button"
              :disabled="isEnrolled(course.id)"
              @click="store.enroll(course)"
            >
              {{
                isEnrolled(course.id)
                  ? 'Enrolled'
                  : 'Enroll'
              }}
            </button>
          </div>
        </div>
      </div>

      <p v-else class="no-results">
        No courses found.
      </p>
    </section>
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import CourseCard from '../components/CourseCard.vue'
import { courses as courseData } from '../data/courses'
import { useEnrollmentStore } from '../stores/enrollment'

const store = useEnrollmentStore()

const courses = ref([])
const searchTerm = ref('')

onMounted(() => {
  courses.value = courseData
})

const filteredCourses = computed(() => {
  const searchValue = searchTerm.value
    .trim()
    .toLowerCase()

  return courses.value.filter((course) =>
    course.name.toLowerCase().includes(searchValue),
  )
})

const isEnrolled = (courseId) =>
  store.enrolledCourses.some(
    (course) => course.id === courseId,
  )
</script>

<style scoped>
.courses-view {
  min-height: calc(100vh - 84px);
  padding: 36px 20px;
  background: linear-gradient(
    rgb(248 250 234 / 88%),
    rgb(244 246 238 / 96%)
  );
}

.courses-section {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
}

.courses-section > h1 {
  position: relative;
  margin-bottom: 28px;
  padding-bottom: 12px;
  color: #20251a;
  text-align: center;
  font-size: 1.8rem;
}

.courses-section > h1::after {
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 70px;
  height: 4px;
  border-radius: 10px;
  background-color: #bfd42f;
  content: '';
  transform: translateX(-50%);
}

.search-container {
  max-width: 500px;
  margin: 0 auto 30px;
  padding: 18px;
  border: 1px solid #e0e5ce;
  border-radius: 10px;
  background-color: #ffffff;
  box-shadow: 0 2px 8px rgb(32 37 26 / 7%);
}

.search-container label {
  display: block;
  margin-bottom: 9px;
  color: #20251a;
  font-weight: 700;
}

.search-container input {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #aeb78b;
  border-radius: 6px;
  background-color: #ffffff;
  color: #20251a;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.search-container input::placeholder {
  color: #747b64;
}

.search-container input:hover {
  border-color: #8c9d16;
}

.search-container input:focus {
  border-color: #718000;
  outline: none;
  box-shadow: 0 0 0 3px rgb(191 212 47 / 28%);
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(
    auto-fit,
    minmax(260px, 1fr)
  );
  gap: 20px;
}

.course-item {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-radius: 10px;
}

.course-item :deep(.course-card) {
  flex: 1;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.course-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  border: 1px solid #d8ddc5;
  border-top: 0;
  border-bottom-right-radius: 10px;
  border-bottom-left-radius: 10px;
  background-color: #ffffff;
}

.details-button,
.enroll-button {
  padding: 12px 10px;
  border: 0;
  font-weight: 700;
  text-align: center;
  text-decoration: none;
}

.details-button {
  border-bottom-left-radius: 9px;
  background-color: #f8faea;
  color: #4d5900;
}

.details-button:hover {
  background-color: #eff5c7;
  color: #4d5900;
}

.enroll-button {
  border-bottom-right-radius: 9px;
  background-color: #bfd42f;
  color: #20251a;
  cursor: pointer;
}

.enroll-button:hover:not(:disabled) {
  background-color: #aabd20;
}

.enroll-button:disabled {
  background-color: #e2e7c2;
  color: #68704d;
  cursor: not-allowed;
}

.details-button:focus,
.enroll-button:focus {
  position: relative;
  z-index: 1;
  outline: 3px solid #718000;
  outline-offset: -3px;
}

.no-results {
  padding: 30px;
  color: #596048;
  text-align: center;
  font-size: 1.1rem;
}

@media (max-width: 400px) {
  .course-actions {
    grid-template-columns: 1fr;
  }

  .details-button {
    border-bottom-left-radius: 0;
  }

  .enroll-button {
    border-bottom-right-radius: 9px;
    border-bottom-left-radius: 9px;
  }
}
</style>