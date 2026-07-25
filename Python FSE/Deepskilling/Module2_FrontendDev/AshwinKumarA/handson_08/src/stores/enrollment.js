import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

export const useEnrollmentStore = defineStore('enrollment', () => {
  const enrolledCourses = ref([])

  const totalCredits = computed(() =>
    enrolledCourses.value.reduce(
      (total, course) => total + course.credits,
      0,
    ),
  )

  const enroll = (course) => {
    const isAlreadyEnrolled = enrolledCourses.value.some(
      (enrolledCourse) => enrolledCourse.id === course.id,
    )

    if (!isAlreadyEnrolled) {
      enrolledCourses.value.push(course)
    }
  }

  const unenroll = (courseId) => {
    enrolledCourses.value = enrolledCourses.value.filter(
      (course) => course.id !== courseId,
    )
  }

  return {
    enrolledCourses,
    totalCredits,
    enroll,
    unenroll,
  }
})