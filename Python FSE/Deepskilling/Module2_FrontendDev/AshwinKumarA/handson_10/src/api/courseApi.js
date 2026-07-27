import apiClient from "./apiClient";
import { courses as localCourses } from "../data/courses";

function transformPostToCourse(post, index = 0) {
  const localCourse =
    localCourses.find((course) => course.id === post.id) ||
    localCourses[index];

  if (localCourse) {
    return {
      ...localCourse,
      description: post.body,
    };
  }

  return {
    id: post.id,
    name: post.title,
    code: `COURSE${String(post.id).padStart(3, "0")}`,
    credits: 3,
    grade: "Not Graded",
    description: post.body,
  };
}

export async function getAllCourses() {
  const posts = await apiClient.get("/posts", {
    params: {
      _limit: 5,
    },
  });

  return posts.map((post, index) =>
    transformPostToCourse(post, index),
  );
}

export async function getCourseById(id) {
  if (!id) {
    throw new Error("A valid course ID is required.");
  }

  const post = await apiClient.get(`/posts/${id}`);

  return transformPostToCourse(post);
}

export async function enrollStudent(studentId, courseId) {
  if (!studentId || !courseId) {
    throw new Error(
      "Student ID and course ID are required for enrollment.",
    );
  }

  const enrollmentData = await apiClient.post("/posts", {
    studentId,
    courseId,
    enrolledAt: new Date().toISOString(),
  });

  return {
    ...enrollmentData,
    studentId,
    courseId,
    enrollmentStatus: "success",
  };
}