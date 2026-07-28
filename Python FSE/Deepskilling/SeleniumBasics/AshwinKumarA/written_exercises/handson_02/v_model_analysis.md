# Hands-On 2: SDLC vs TDLC – V-Model & Agile QA Integration

**Program:** Digital Nurture 5.0  
**Track:** Python Full Stack Engineer  
**Module:** QA Concepts & Selenium Basics  
**Author:** Ashwin Kumar A  

---

# Task 1: V-Model Mapping

## 1. V-Model Diagram (ASCII)

```text
Requirements                Acceptance Testing
      \                           /
       \                         /
    System Design          System Testing
         \                 /
          \               /
   Architecture Design  Integration Testing
            \          /
             \        /
         Module Design
                |
             Coding
                |
           Unit Testing
```

---

## 2. SDLC Phase ↔ TDLC Phase Mapping

| SDLC Phase | TDLC Phase | Test Artifact Prepared |
|------------|------------|------------------------|
| Requirements | Acceptance Testing | Acceptance Test Plan |
| System Design | System Testing | System Test Cases |
| Architecture Design | Integration Testing | Integration Test Plan |
| Module Design | Unit Testing | Unit Test Cases |
| Coding | Execution | Source Code and Unit Test Execution |

---

## 3. Entry and Exit Criteria

| Testing Level | Entry Criteria | Exit Criteria |
|---------------|---------------|---------------|
| Unit Testing | Module is developed | All unit tests pass and critical defects are fixed |
| Integration Testing | Modules are unit tested | Integrated components work correctly and major defects are fixed |
| System Testing | Complete application is deployed | All planned system test cases are executed with no open critical defects |
| Acceptance Testing | System testing is completed | Customer accepts the application for release |

---

## 4. QA Involvement in the V-Model

1. **Requirements Phase**
   - QA reviews requirements for clarity, completeness, and testability.

2. **System Design Phase**
   - QA prepares the test strategy and identifies test scenarios before development begins.

---

# Task 2: Agile QA and Shift-Left Testing

## 5. Problems in the Waterfall Model

1. Defects are found late, making them expensive to fix.
2. Testing starts only after development is completed, causing project delays.
3. Requirement issues may remain unnoticed until final testing.

---

## 6. QA Role in Agile Ceremonies

| Agile Ceremony | QA Responsibility |
|----------------|------------------|
| Sprint Planning | Review user stories and define acceptance criteria |
| Daily Stand-up | Report testing progress and discuss blockers |
| Sprint Review | Validate completed features and demonstrate testing results |
| Retrospective | Suggest improvements to the testing process |

---

## 7. Shift-Left Testing Practices

| Practice | Application to Course Management API |
|----------|--------------------------------------|
| Review requirements | Verify requirements are complete and testable before development |
| Write test cases early | Prepare test cases before coding begins |
| Static code analysis | Detect coding issues before execution |
| API contract testing | Validate API request and response formats before integration |

---

## 8. Acceptance Criteria (Given-When-Then)

### Scenario 1 – Successful Course Creation

```text
Given the college admin is on the Create Course page
When valid course details are entered
Then the course should be created successfully.
```

### Scenario 2 – Duplicate Course Code

```text
Given a course code already exists
When the admin creates another course using the same code
Then an appropriate duplicate course error should be displayed.
```

### Scenario 3 – Missing Required Fields

```text
Given the Create Course page is open
When mandatory fields are left blank
Then validation messages should be displayed and the course should not be created.
```

---

# Conclusion

This hands-on demonstrates the relationship between SDLC and TDLC using the V-Model, explains QA activities in Agile, introduces the Shift-Left testing approach, and defines acceptance criteria using the Given–When–Then format.
