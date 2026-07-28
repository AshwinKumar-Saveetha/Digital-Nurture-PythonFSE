# Hands-On 3: Test Automation Process, Lifecycle & Framework Types

**Program:** Digital Nurture 5.0  
**Track:** Python Full Stack Engineer  
**Module:** QA Concepts & Selenium Basics  
**Author:** Ashwin Kumar A  

---

## Task 1: Automation Decision and Test Case Selection

### 1. Criteria for Deciding Whether a Test Case Should Be Automated

Test scenario: Verify that `POST /api/courses/` returns status code `201` with the correct course data when valid input is provided.

| Criterion | Explanation | Application to the Test Scenario |
|---|---|---|
| Repetitive execution | Tests that are executed frequently are good candidates for automation. | This test can be run after every code change to confirm that course creation still works. |
| Regression importance | Important existing functionality should be checked after changes. | Course creation is a core feature, so it should be included in regression testing. |
| Stable requirements | Tests with stable inputs and expected results are easier to automate and maintain. | The valid request, `201` response, and course data validation are clearly defined. |
| Data-driven testing | Tests that need to run with multiple input values benefit from automation. | The same test can run with different course names, codes, durations, and fees. |
| Business risk | High-risk and business-critical features should be tested regularly. | Failure of the course creation endpoint would prevent administrators from adding courses. |

**Decision:** This test case should be automated because it is repetitive, stable, important for regression testing, data-driven, and business-critical.

---

### 2. Automate or Manual Decision

| Test Case | Decision | Justification |
|---|---|---|
| Regression test for all CRUD endpoints after every code change | Automate | It is repetitive, time-consuming, and must be executed frequently. |
| Exploratory testing of a new search feature | Manual | Exploratory testing requires human observation, creativity, and investigation. |
| Performance test with 100 concurrent users calling `GET /api/courses/` | Automate | Automation tools can create concurrent users and measure performance accurately. |
| UI test for the login form | Automate | Login is a stable and frequently used feature that should be included in regression testing. |
| Verify that the Swagger API documentation is accurate | Manual | Documentation requires human review to confirm clarity, wording, and correctness. |
| Smoke test to verify that the API is reachable after deployment | Automate | It is a simple, repetitive check that should run after every deployment. |

---

### 3. Test Automation ROI

Test Automation ROI measures whether the time and effort saved by automation are greater than the time and cost required to create and maintain the automated test.

Given:

- Automation development time = 4 hours
- Manual execution time per run = 30 minutes = 0.5 hour

```text
Break-even runs = Automation development time / Manual execution time per run

Break-even runs = 4 / 0.5

Break-even runs = 8
```

The automated test pays for itself after **8 runs**.

A 20% maintenance overhead applies only after the 10th run. Therefore, it does not affect the initial break-even point of 8 runs. After the 10th run, maintenance effort should be included when calculating future savings.

---

### 4. Flaky Tests

A flaky test is an automated test that sometimes passes and sometimes fails even when the application code has not changed.

#### Example

A Selenium test clicks a button before it becomes fully visible. On a fast system the test passes, but on a slow system it fails with an element-not-found or element-not-clickable error.

#### Strategies to Prevent or Fix Flaky Tests

1. Use explicit waits instead of fixed `time.sleep()` statements.
2. Use stable and unique locators such as ID or reliable CSS selectors.
3. Keep tests independent and reset test data before each execution.

---

## Task 2: Compare Automation Framework Types

### 5. Linear Framework

A Linear framework records or writes test steps in a direct sequence. Each test script contains all actions, test data, and validations in one file.

**Advantage:** Simple to create and easy for beginners to understand.

**Disadvantage:** Code is difficult to reuse and maintain when the number of tests increases.

**Course Management Example:** Use it for a small script that opens the login page, enters credentials, and verifies successful login.

---

### 6. Modular Framework

A Modular framework divides the application into separate reusable modules. Common actions such as login, course creation, and logout are written once and reused in multiple tests.

**Advantage:** Reduces code duplication and improves maintainability.

**Disadvantage:** Requires proper planning and more initial setup.

**Course Management Example:** Create separate modules for login, course creation, course update, and course deletion.

---

### 7. Data-Driven Framework

A Data-Driven framework separates test data from test scripts. The same test is executed multiple times using data from files such as CSV, JSON, or Excel.

**Advantage:** Supports testing with many input combinations without duplicating test code.

**Disadvantage:** Test data files must be maintained carefully.

**Course Management Example:** Test course creation using multiple course names, course codes, durations, and fees stored in a data file.

---

### 8. Keyword-Driven Framework

A Keyword-Driven framework uses keywords such as `OpenBrowser`, `EnterText`, `Click`, and `VerifyText` to describe test actions. The keywords are connected to reusable functions.

**Advantage:** Non-technical team members can understand and prepare tests using predefined keywords.

**Disadvantage:** Creating and maintaining the keyword library requires additional effort.

**Course Management Example:** A test can use keywords such as `Login`, `CreateCourse`, and `VerifyCourseCreated`.

---

### 9. Hybrid Framework

A Hybrid framework combines features from two or more frameworks, usually Modular, Data-Driven, and Keyword-Driven frameworks.

**Advantage:** Provides reusability, flexibility, and support for multiple test data sets.

**Disadvantage:** It is more complex to design and maintain than a simple framework.

**Course Management Example:** Use reusable page modules, external login data, and readable keywords for the complete Course Management frontend test suite.

---

### 10. Recommended Framework

The recommended framework is a **Hybrid Framework** combining:

- **Data-Driven Framework** to test 50 username and password combinations.
- **Modular Framework** to reuse login steps across 20 test cases.
- **Keyword-Driven Framework** to allow technical and non-technical team members to understand and prepare tests.

This combination reduces duplication, supports multiple test data sets, and makes the test suite easier for different team members to use.

---

### 11. Hybrid Framework Folder Structure

```text
course_management_automation/
│
├── config/
│   └── config.json
│
├── test_data/
│   └── login_data.csv
│
├── pages/
│   ├── login_page.py
│   └── course_page.py
│
├── utilities/
│   └── driver_setup.py
│
├── tests/
│   ├── test_login.py
│   └── test_course_management.py
│
├── requirements.txt
└── README.md
```

#### Folder Description

| Folder/File | Purpose |
|---|---|
| `config/` | Stores configuration such as base URL and browser name. |
| `test_data/` | Stores input data used by data-driven tests. |
| `pages/` | Stores reusable page objects and page actions. |
| `utilities/` | Stores common helper functions and WebDriver setup. |
| `tests/` | Stores test cases and assertions. |
| `requirements.txt` | Lists required Python packages. |
| `README.md` | Explains project setup and test execution. |
