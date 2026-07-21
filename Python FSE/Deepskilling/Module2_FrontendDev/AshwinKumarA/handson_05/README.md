# Hands-On 5 -- Student Portal (React)

## Overview

This project implements a **Student Portal** using **React + Vite**. The
application demonstrates React components, props, state management,
event handling, filtering, `useEffect()`, API integration, and
component-based UI development.

------------------------------------------------------------------------

# Technologies Used

-   React
-   Vite
-   JavaScript (ES6)
-   HTML5
-   CSS3

------------------------------------------------------------------------

# Project Structure

``` text
student-portal-react/
│
├── images/
│   ├── task1-student-portal-home.png
│   ├── task2-search-course.png
│   ├── task2-enroll-course.png
│   ├── multiple-enrollments.png
│   ├── duplicate-enrollment-alert.png
│   ├── task3-loading.png
│   ├── task3-notifications.png
│   ├── task3-student-profile.png
│   └── task3-final-output.png
│
├── src/
├── public/
├── package.json
└── README.md
```

------------------------------------------------------------------------

# Task 1 (PDF Steps 60--65)

## Features Implemented

-   Created React application using Vite
-   Removed default Vite boilerplate
-   Created reusable Header component
-   Created reusable Footer component
-   Created reusable CourseCard component
-   Passed `siteName` using props

## Screenshot

![Task 1](images/task1-student-portal-home.png)

------------------------------------------------------------------------

# Task 2 (PDF Steps 66--70)

## Features Implemented

-   Implemented `useState`
-   Stored course data in state
-   Added search functionality
-   Added Enroll button
-   Maintained enrolled course count
-   Prevented duplicate enrollment

### Screenshot 1 -- Search

![Search](images/task2-search-course.png)

------------------------------------------------------------------------

### Screenshot 2 -- Enroll Course

![Enroll](images/task2-enroll-course.png)

------------------------------------------------------------------------

### Screenshot 3 -- Multiple Enrollments

![Multiple Enrollments](images/multiple-enrollments.png)

------------------------------------------------------------------------

### Screenshot 4 -- Duplicate Enrollment Alert

![Duplicate Alert](images/duplicate-enrollment-alert.png)

------------------------------------------------------------------------

# Task 3 (PDF Steps 71--75)

## Features Implemented

-   Used `useEffect()` to fetch notifications from JSONPlaceholder
-   Displayed loading message while fetching
-   Added API error handling
-   Created `StudentProfile` component using `useState`
-   Used empty dependency array (`[]`) so API runs once on page load

### Screenshot 1 -- Loading State

![Loading](images/task3-loading.png)

------------------------------------------------------------------------

### Screenshot 2 -- Notifications Loaded

![Notifications](images/task3-notifications.png)

------------------------------------------------------------------------

### Screenshot 3 -- Student Profile

![Student Profile](images/task3-student-profile.png)

------------------------------------------------------------------------

### Screenshot 4 -- Final Output

![Final Output](images/task3-final-output.png)

------------------------------------------------------------------------

# How to Run

``` bash
npm install
npm run dev
```

Open:

    http://localhost:5173

------------------------------------------------------------------------

# Learning Outcomes

-   React Components
-   Props
-   useState Hook
-   useEffect Hook
-   Event Handling
-   Search Filtering
-   Conditional Rendering
-   API Fetching
-   Component Reusability

------------------------------------------------------------------------

# Author

**Ashwin Kumar A**

Frontend Development Hands-On 5
