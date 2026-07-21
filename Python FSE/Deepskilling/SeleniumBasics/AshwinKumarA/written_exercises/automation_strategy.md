# Test Automation Process, Lifecycle & Framework Types
**Hands-On 3 Submission**  
**Author:** Ashwin Kumar A


# Task 1: Automation Decision and Test Case Selection

## 17. Five Automation Decision Criteria

| Criterion | Explanation | Application to POST /api/courses/ |
|---|---|---|
| Repetitive Execution | Frequently executed tests should be automated. | Regression execution after every build. |
| Stable Functionality | Stable features are suitable for automation. | API endpoint is stable. |
| High Business Risk | Critical functionality deserves automation. | Course creation is business critical. |
| Data-Driven | Multiple input combinations. | Different course inputs can be tested automatically. |
| Time Saving | Reduces manual effort. | Saves execution time across releases. |

## 18. Automate or Manual

| Test Case | Decision | Reason |
|---|---|---|
| CRUD Regression | Automate | Executed repeatedly |
| Exploratory Testing | Manual | Requires human analysis |
| Performance Test | Automate | Tool-based execution |
| Login UI Test | Automate | Stable repetitive scenario |
| Swagger Documentation | Manual | Visual verification |
| Smoke Test | Automate | Run after every deployment |

## 19. Test Automation ROI

Automation effort = 4 hours

Manual execution = 30 minutes

Break-even = 8 executions

After the 10th run, include 20% maintenance overhead while calculating future savings.

## 20. Flaky Test

A flaky test produces inconsistent results without application changes.

Example:
A Selenium test fails because the element loads slowly.

Prevention:
1. Use Explicit Waits.
2. Avoid hard-coded sleep().
3. Use reliable locators.

# Task 2: Compare Automation Framework Types

## 21. Framework Comparison

| Framework | Description | Advantage | Disadvantage | Course Management Example |
|---|---|---|---|---|
| Linear | Sequential scripts | Easy | Poor reuse | Small demo |
| Modular | Reusable modules | Easy maintenance | Initial effort | Login module reuse |
| Data-Driven | External test data | Multiple datasets | Data management | API validation |
| Keyword-Driven | Keywords control execution | Non-programmers can use | Complex setup | Business testers |
| Hybrid | Combination of frameworks | Flexible & scalable | Higher complexity | Enterprise automation |

## 22. Recommended Framework

Hybrid Framework combining:
- Modular Framework
- Data-Driven Framework
- Keyword-Driven Framework

Reason:
Supports reusable login steps, multiple datasets, and both technical and non-technical team members.

## 23. Hybrid Framework Folder Structure

```text
CourseManagementAutomation/
│
├── config/
├── pages/
├── tests/
├── testdata/
├── utilities/
├── reports/
├── screenshots/
├── requirements.txt
└── README.md
```

This structure improves maintainability, scalability, and reusability.
