import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  enrolledCourses: []
};

const enrollmentSlice = createSlice({
  name: "enrollment",
  initialState,

  reducers: {
    enroll: (state, action) => {
      const course = action.payload;

      const alreadyEnrolled = state.enrolledCourses.some(
        (item) => item.id === course.id
      );

      if (!alreadyEnrolled) {
        state.enrolledCourses.push(course);
      }
    },

    unenroll: (state, action) => {
      const courseId = action.payload;

      state.enrolledCourses =
        state.enrolledCourses.filter(
          (course) => course.id !== courseId
        );
    }
  }
});

export const { enroll, unenroll } =
  enrollmentSlice.actions;

export default enrollmentSlice.reducer;