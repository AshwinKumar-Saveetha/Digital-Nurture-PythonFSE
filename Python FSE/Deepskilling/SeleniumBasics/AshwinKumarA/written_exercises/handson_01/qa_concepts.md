# Hands-On 1: QA Concepts, Functional Testing & Defect Lifecycle

**Program:** Digital Nurture 5.0  
**Track:** Python Full Stack Engineer  
**Module:** QA Concepts & Selenium Basics  
**Author:** Ashwin Kumar A  

---

## Task 1: Map Testing Types to a Real System

### 1. Testing Levels for the Course Management API

| Testing Type | Test Case | Classification |
|---|---|---|
| Unit Testing | Test the course creation validation function with valid course data and verify that it returns a valid course object. | Functional |
| Integration Testing | Send a valid request to `POST /api/courses/` and verify that the API stores the course correctly in the database. | Functional |
| System Testing | Create a course through the API, retrieve it using `GET /api/courses/`, and verify that the complete course details are returned correctly from the database. | Functional |
| User Acceptance Testing | A college administrator creates a new course using valid details and verifies that the course is available for student enrolment. | Functional |

### 2. Non-Functional Test Example

#### Performance Testing

Send multiple requests to `GET /api/courses/` and verify that the API returns the course list within an acceptable response time.

**Expected Result:** The API should return a successful response within the defined response-time limit without errors.

---

### 3. Black-Box Testing vs White-Box Testing

| Black-Box Testing | White-Box Testing |
|---|---|
| Testing is performed without knowledge of the internal code. | Testing is performed with knowledge of the internal code and logic. |
| It focuses on inputs, outputs, and expected behaviour. | It focuses on code paths, conditions, loops, and internal logic. |
| It is usually performed by QA testers. | It is usually performed by developers. |
| Example: Sending a request to `POST /api/courses/` and checking the response. | Example: Testing every condition inside the course validation function. |

A QA tester typically performs black-box testing because the tester checks whether the application behaves according to the requirements.

A developer typically performs white-box testing because the developer understands the internal code and can test individual functions, branches, and conditions.

---

### 4. Formal Test Cases for `POST /api/courses/`

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC_COURSE_001 | Create a course using valid details | API server is running and the course code does not already exist | 1. Open the API testing tool. 2. Select the `POST` method. 3. Enter `/api/courses/`. 4. Provide valid course details. 5. Send the request. | The API should return status code `201 Created` and the response should contain the newly created course details. |  |  |
| TC_COURSE_002 | Create a course without a required field | API server is running | 1. Open the API testing tool. 2. Select the `POST` method. 3. Enter `/api/courses/`. 4. Omit a required field such as course name. 5. Send the request. | The API should reject the request and return a validation error with an appropriate client error status code. |  |  |
| TC_COURSE_003 | Create a course with an existing course code | API server is running and a course with the same code already exists | 1. Open the API testing tool. 2. Select the `POST` method. 3. Enter `/api/courses/`. 4. Provide a course code that already exists. 5. Send the request. | The API should reject the request and return an error stating that the course code already exists. |  |  |

---

## Task 2: Defect Lifecycle & Severity Classification

### 5. Defect Lifecycle

```text
New
  |
  v
Assigned
  |
  v
Open
  |
  v
Fixed
  |
  v
Retest
  |
  v
Verified
  |
  v
Closed
```

#### Defect States

- **New:** A tester identifies and reports a defect.
- **Assigned:** The defect is assigned to a developer.
- **Open:** The developer analyses and starts working on the defect.
- **Fixed:** The developer fixes the defect and marks it ready for testing.
- **Retest:** The tester tests the defect again in the updated build.
- **Verified:** The tester confirms that the defect is fixed.
- **Closed:** The defect is closed after successful verification.

#### Rejected Path

A defect may be marked as **Rejected** if it is not a valid defect, cannot be reproduced, is working as designed, or is caused by incorrect test data.

```text
New / Assigned
      |
      v
   Rejected
```

#### Deferred Path

A valid defect may be marked as **Deferred** when the team decides to fix it in a future release because it is not urgent or because of time and resource limitations.

```text
Open
 |
 v
Deferred
```

If the defect fails during retesting, it can be reopened and assigned again for correction.

```text
Retest
  |
  v
Reopened
  |
  v
Assigned
```

---

### 6. Severity and Priority Classification

| Bug | Severity | Priority | Justification |
|---|---|---|---|
| `POST /api/courses/` returns `500 Internal Server Error` for all requests. | Critical | P1 | The main course creation function is completely unavailable. It blocks users from creating courses and requires immediate correction. |
| Course names longer than 150 characters are silently truncated without an error. | Medium | P2 | The API continues to work, but data may be saved incorrectly without informing the user. It should be fixed before the next release. |
| The `/docs` Swagger page has a typo in the API description. | Low | P4 | The defect is only a documentation issue and does not affect API functionality. |
| Login with correct credentials occasionally returns `401` on the first attempt. | High | P1 | Valid users may be unable to log in. The intermittent behaviour indicates instability and should be investigated urgently. |

---

### 7. Defect Report

| Field | Details |
|---|---|
| Defect ID | DEF_COURSE_001 |
| Title | `POST /api/courses/` returns `500 Internal Server Error` for all valid requests |
| Environment | Windows 11, Google Chrome, Course Management API test environment |
| Build Version | Build 1.0 |
| Severity | Critical |
| Priority | P1 |
| Steps to Reproduce | 1. Start the Course Management API. 2. Open an API testing tool. 3. Select the `POST` method. 4. Enter `/api/courses/`. 5. Provide valid course details. 6. Send the request. |
| Expected Result | The API should create the course and return status code `201 Created` with the course details. |
| Actual Result | The API returns status code `500 Internal Server Error`. |
| Attachments | Screenshot of 500 error |

---

### 8. Difference Between Severity and Priority

| Severity | Priority |
|---|---|
| Severity shows how seriously the defect affects the system. | Priority shows how urgently the defect must be fixed. |
| It is based on technical and business impact. | It is based on release needs and business urgency. |
| Common levels are Critical, High, Medium, and Low. | Common levels are P1, P2, P3, and P4. |

#### Example: High Severity but Low Priority

A major failure occurs in an old reporting feature that is no longer used by customers.

The defect has **High Severity** because the feature does not work at all. However, it may have **Low Priority** because the feature is rarely used and is planned for removal in a future release.
