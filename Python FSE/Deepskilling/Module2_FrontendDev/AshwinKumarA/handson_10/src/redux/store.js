import { configureStore } from "@reduxjs/toolkit";

import enrollmentReducer from "./enrollmentSlice";
import courseReducer from "./courseSlice";

export const store = configureStore({
  reducer: {
    enrollment: enrollmentReducer,
    courses: courseReducer,
  },
});