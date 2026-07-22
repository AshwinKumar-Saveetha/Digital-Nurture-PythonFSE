# Student Portal React Application

## Hands-On 06

**Author:** Ashwin Kumar A

This Hands-On extends the Student Portal React application by implementing React Router, Context API and Redux Toolkit. The application allows students to browse courses, view course details, enroll in courses and manage enrolled courses using global state management.

---

# Task 1 – React Router

React Router DOM v6 was installed and configured. The application was wrapped using `BrowserRouter` and separate pages were created for Home, Courses, Course Details and Profile.

## React Router Installation

![React Router Installed](screenshots/HS6_Task1_01_React_Router_Installed.png)

React Router was successfully installed and verified.

## Routing Configuration

![Routing Configuration](screenshots/HS6_Task1_02_Routing_Code.png)

Routes were created using `Routes` and `Route`. Navigation between pages is performed using `Link`.

## Dynamic Course Details

![Course Details](screenshots/HS6_Task1_03_Course_Details.png)

Dynamic routing was implemented using `useParams()` to display the selected course information.

## Profile Redirection

![Profile Redirect](screenshots/HS6_Task1_04_Enroll_Profile_Redirect.png)

After enrolling in a course, `useNavigate()` redirects the user to the Profile page.

---

# Task 2 – Context API

A Context Provider was created to share enrollment information across multiple components without prop drilling.

## Enrollment Context

![Enrollment Context](screenshots/HS6_Task2_01_Enrollment_Context.png)

The provider stores enrolled courses and exposes enroll and remove functions.

## Shared State

![Context Shared State](screenshots/HS6_Task2_02_Context_Shared_State.png)

The Header and Profile page access the same shared state using `useContext()`.

## Remove Course

![Remove Course](screenshots/HS6_Task2_03_Remove_Course.png)

Students can remove enrolled courses directly from the Profile page.

---

# Task 3 – Redux Toolkit

The Context implementation was replaced with Redux Toolkit for centralized state management.

## Redux Setup

![Redux Setup](screenshots/HS6_Task3_01_Redux_Setup.png)

A Redux Store and Enrollment Slice were created using `configureStore()` and `createSlice()`.

## Shared Redux State

![Redux Shared State](screenshots/HS6_Task3_02_Redux_Shared_State.png)

Components access Redux state using `useSelector()` and update it using `useDispatch()`.

## Redux DevTools

![Redux DevTools](screenshots/HS6_Task3_03_Redux_DevTools.png)

Redux DevTools confirms that enroll and unenroll actions are dispatched successfully.

---

# Final Output

![Final Output](screenshots/HS6_Final_Output.png)

The completed Student Portal application supports routing, dynamic pages, enrollment management and centralized state management using Redux Toolkit.

---


# Author

**Ashwin Kumar A**

Digital Nurture 5.0

Frontend Development – Hands-On 06
