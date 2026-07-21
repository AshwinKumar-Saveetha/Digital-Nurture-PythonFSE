# SDLC vs TDLC — V-Model & Agile QA Integration
**Hands-On 2 Submission**  
**Author:** Ashwin Kumar A

# Task 1: V-Model Mapping

## 9. V-Model

```
Requirements            <-> Acceptance Testing
System Design           <-> System Testing
Architecture Design     <-> Integration Testing
Module Design           <-> Unit Testing
            Coding
```

## 10. SDLC ↔ TDLC Artifacts

| SDLC Phase | TDLC Phase | Test Artifact |
|---|---|---|
| Requirements | Acceptance Testing | Acceptance Test Plan |
| System Design | System Testing | System Test Cases |
| Architecture Design | Integration Testing | Integration Test Cases |
| Module Design | Unit Testing | Unit Test Cases |

## 11. Entry & Exit Criteria

### Unit Testing
- Entry: Module completed.
- Exit: All unit tests pass, no critical defects.

### Integration Testing
- Entry: Modules integrated.
- Exit: Interfaces verified, major defects fixed.

### System Testing
- Entry: Complete application deployed in QA.
- Exit: Functional and non-functional tests completed.

### Acceptance Testing
- Entry: System testing completed.
- Exit: Customer approval obtained.

## 12. Early QA Engagement

1. Requirements review to remove ambiguities.
2. Design review to identify testability issues.

# Task 2: Agile QA & Shift-Left Testing

## 13. Three Waterfall Problems

1. Defects found late.
2. High fixing cost.
3. Delivery delays.

## 14. QA Role in Agile

| Ceremony | QA Activity |
|---|---|
| Sprint Planning | Define acceptance criteria |
| Daily Stand-up | Report blockers and testing progress |
| Sprint Review | Validate completed features |
| Retrospective | Suggest process improvements |

## 15. Shift-Left Practices

1. Review requirements for testability.
2. Write test cases before coding (TDD/BDD).
3. Static code analysis.
4. API contract testing before integration.

## 16. Acceptance Criteria (Given-When-Then)

### Happy Path
**Given** valid course details  
**When** the admin submits the course  
**Then** the course is created successfully.

### Duplicate Course Code
**Given** an existing course code  
**When** the admin submits the same code  
**Then** an appropriate duplicate error is displayed.

### Missing Required Fields
**Given** mandatory fields are empty  
**When** the admin submits the form  
**Then** validation errors are displayed.
