import {
  createAsyncThunk,
  createSlice,
} from "@reduxjs/toolkit";

import { getAllCourses } from "../api/courseApi";

export const fetchAllCourses = createAsyncThunk(
  "courses/fetchAll",
  async () => {
    return await getAllCourses();
  },
);

const initialState = {
  courses: [],
  loading: false,
  error: "",
};

const courseSlice = createSlice({
  name: "courses",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchAllCourses.pending, (state) => {
        state.loading = true;
        state.error = "";
      })
      .addCase(
        fetchAllCourses.fulfilled,
        (state, action) => {
          state.courses = action.payload;
          state.loading = false;
          state.error = "";
        },
      )
      .addCase(
        fetchAllCourses.rejected,
        (state, action) => {
          state.loading = false;
          state.error =
            action.error.message ||
            "Unable to load courses.";
        },
      );
  },
});

export const selectCourses = (state) =>
  state.courses.courses;

export const selectCoursesLoading = (state) =>
  state.courses.loading;

export const selectCoursesError = (state) =>
  state.courses.error;

export default courseSlice.reducer;