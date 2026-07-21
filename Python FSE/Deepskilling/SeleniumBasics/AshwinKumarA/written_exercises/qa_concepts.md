# QA Concepts & Functional Testing & Defect Lifecycle
**Hands-On 1 Submission**  
**Author:** Ashwin Kumar A

> This submission is prepared as a student's work based strictly on the tasks in the Selenium Basics Hands-On Exercise Book.

# Task 1: Map Testing Types to a Real System

## 1. Test Levels

### Unit Testing
Test the validation function that checks whether the course code is unique before saving.

**Type:** Functional

### Integration Testing
Verify that the POST `/api/courses/` endpoint stores a valid course in the database and returns HTTP 201.

**Type:** Functional

### System Testing
Create a course through the API and verify it is stored and retrieved successfully.

**Type:** Functional

### User Acceptance Testing (UAT)
A college administrator creates a course and confirms it appears correctly for student enrollment.

**Type:** Functional

## 2. Non-Functional Test Example

Performance Test: Verify the API can handle 500 concurrent users while maintaining acceptable response time.

## 3. Black-Box vs White-Box Testing

| Black-Box Testing | White-Box Testing |
|---|---|
| Tests external functionality without source code knowledge. | Tests internal code, logic, branches and paths. |
| Usually performed by QA testers. | Usually performed by developers. |

## 4. Test Cases

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC001 | Create course with valid data | API running | Send valid POST request | 201 Created | | |
| TC002 | Create duplicate course | Existing course code | Send duplicate POST | Duplicate error returned | | |
| TC003 | Missing mandatory field | API running | Send POST without course name | Validation error returned | | |

# Task 2: Defect Lifecycle & Severity Classification

## 5. Defect Lifecycle

New → Assigned → Open → Fixed → Retest → Verified → Closed

Rejected: Bug is invalid or cannot be reproduced.

Deferred: Bug fix postponed to a future release.

## 6. Severity & Priority

| Bug | Severity | Priority | Justification |
|---|---|---|---|
| POST returns 500 for all requests | Critical | P1 | API completely unusable |
| Long names truncated | Medium | P2 | Data integrity issue |
| Swagger typo | Low | P4 | Cosmetic issue |
| Login occasionally returns 401 | High | P1 | Intermittent authentication failure |

## 7. Defect Report

- **Defect ID:** DEF-001
- **Title:** POST /api/courses/ returns HTTP 500
- **Environment:** QA
- **Build Version:** v1.0
- **Severity:** Critical
- **Priority:** P1
- **Steps to Reproduce:**
  1. Start API.
  2. Send valid POST request.
  3. Observe response.
- **Expected Result:** Course created with HTTP 201.
- **Actual Result:** HTTP 500 Internal Server Error.
- **Attachments:** Screenshot of 500 error.

## 8. Severity vs Priority

Severity measures the impact of a defect, whereas Priority measures how urgently it should be fixed.

Example: A spelling mistake on the CEO dashboard has Low Severity but High Priority because it is highly visible.
