<template>
  <main class="detail-view">
    <section v-if="selectedCourse" class="detail-card">
      <p class="course-code">{{ selectedCourse.code }}</p>

      <h1>{{ selectedCourse.name }}</h1>

      <p class="description">
        {{ selectedCourse.description }}
      </p>

      <div class="course-information">
        <p>
          <strong>Credits:</strong>
          {{ selectedCourse.credits }}
        </p>

        <p>
          <strong>Grade:</strong>
          {{ selectedCourse.grade }}
        </p>
      </div>

      <div class="actions">
        <RouterLink class="back-button" to="/courses">
          Back to Courses
        </RouterLink>

        <button class="enroll-button" type="button" @click="handleEnroll">
          Enroll
        </button>
      </div>
    </section>

    <section v-else class="not-found-card">
      <h1>Course Not Found</h1>

      <p>The requested course does not exist.</p>

      <RouterLink class="back-button" to="/courses">
        Back to Courses
      </RouterLink>
    </section>
  </main>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { courses } from '../data/courses'

const route = useRoute()
const router = useRouter()

const selectedCourse = computed(() => {
  const courseId = Number(route.params.id)

  return courses.find((course) => course.id === courseId)
})

const handleEnroll = () => {
  router.push('/profile')
}
</script>

<style scoped>
.detail-view {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 84px);
  padding: 40px 20px;
  background-color: #f4f6ee;
}

.detail-card,
.not-found-card {
  width: 100%;
  max-width: 720px;
  padding: 36px;
  border: 1px solid #d8ddc5;
  border-top: 7px solid #bfd42f;
  border-radius: 12px;
  background-color: #ffffff;
  box-shadow: 0 8px 24px rgb(32 37 26 / 12%);
}

.course-code {
  margin-bottom: 8px;
  color: #718000;
  font-weight: 700;
  letter-spacing: 1px;
}

.detail-card h1,
.not-found-card h1 {
  margin-bottom: 18px;
  color: #20251a;
  font-size: 2rem;
}

.description {
  margin-bottom: 24px;
  color: #596048;
  line-height: 1.7;
}

.course-information {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
  padding: 18px;
  border-radius: 8px;
  background-color: #f8faea;
}

.course-information p {
  color: #454b39;
}

.course-information strong {
  color: #20251a;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.back-button,
.enroll-button {
  padding: 12px 20px;
  border-radius: 7px;
  font-weight: 700;
  text-decoration: none;
}

.back-button {
  border: 1px solid #718000;
  background-color: #ffffff;
  color: #4d5900;
}

.back-button:hover {
  background-color: #eff5c7;
  color: #4d5900;
}

.enroll-button {
  border: 1px solid #bfd42f;
  background-color: #bfd42f;
  color: #20251a;
  cursor: pointer;
}

.enroll-button:hover {
  border-color: #aabd20;
  background-color: #aabd20;
}

.back-button:focus,
.enroll-button:focus {
  outline: 3px solid #718000;
  outline-offset: 3px;
}

.not-found-card p {
  margin-bottom: 24px;
  color: #596048;
}

@media (max-width: 500px) {
  .course-information {
    flex-direction: column;
    gap: 12px;
  }
}
</style>