-- ============================================================
-- Digital Nurture 5.0 - Module 3: Database Integration
-- HANDS-ON 3 [Intermediate]
-- Advanced SQL - Subqueries, Views & Transactions
-- Engine: MySQL 8.x
-- Prerequisite: run hands_on_1.sql then hands_on_2.sql first
-- ============================================================

USE college_db;

-- --------------------------------------------------------------
-- TASK 1: Subqueries
-- --------------------------------------------------------------

-- Step 35: students enrolled in more courses than the average
-- number of enrollments per student (non-correlated subquery
-- calculates the average once, then the outer query filters on it)
SELECT student_id, COUNT(*) AS course_count
FROM enrollments
GROUP BY student_id
HAVING COUNT(*) > (
    SELECT AVG(cnt) FROM (
        SELECT COUNT(*) AS cnt
        FROM enrollments
        GROUP BY student_id
    ) AS per_student_counts
);

-- Step 36: courses where every enrolled student received an 'A'.
-- Uses NOT EXISTS: a course qualifies only if there is no
-- enrollment row for it whose grade is anything other than 'A'.
SELECT c.course_id, c.course_name
FROM courses c
WHERE EXISTS (
    SELECT 1 FROM enrollments e WHERE e.course_id = c.course_id
)
AND NOT EXISTS (
    SELECT 1 FROM enrollments e
    WHERE e.course_id = c.course_id
    AND (e.grade <> 'A' OR e.grade IS NULL)
);

-- Step 37: the professor with the highest salary in each
-- department (correlated subquery - re-evaluated per outer row)
SELECT p.*
FROM professors p
WHERE p.salary = (
    SELECT MAX(p2.salary)
    FROM professors p2
    WHERE p2.department_id = p.department_id
);

-- Step 38: derived table (subquery in the FROM clause) - compute
-- per-department average salary, then filter to departments
-- where that average exceeds 85,000. Derived tables must be aliased.
SELECT dept_avg.department_id, dept_avg.avg_salary
FROM (
    SELECT department_id, AVG(salary) AS avg_salary
    FROM professors
    GROUP BY department_id
) AS dept_avg
WHERE dept_avg.avg_salary > 85000;


-- --------------------------------------------------------------
-- TASK 2: Creating and Using Views
-- --------------------------------------------------------------

-- Step 39: each student's full name, department, number of
-- enrolled courses, and GPA (A=4, B=3, C=2, D=1, F=0)
CREATE OR REPLACE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    CONCAT(s.first_name,' ',s.last_name) AS full_name,
    d.dept_name,
    COUNT(e.enrollment_id) AS courses_enrolled,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
            ELSE NULL
        END
    ),2) AS gpa
FROM students s
LEFT JOIN departments d ON s.department_id = d.department_id
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, full_name, d.dept_name;

-- Step 40: course_name, course_code, total_enrollments, avg_gpa
CREATE OR REPLACE VIEW vw_course_stats AS
SELECT
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
            ELSE NULL
        END
    ),2) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;

-- Step 41: students with GPA above 3.0
SELECT * FROM vw_student_enrollment_summary WHERE gpa > 3.0;

-- Step 42: attempting to UPDATE through vw_student_enrollment_summary
-- will fail with: "The target table vw_student_enrollment_summary
-- of the UPDATE is not updatable." This is expected because the
-- view aggregates data (COUNT/AVG) and joins multiple base tables -
-- MySQL (and the SQL standard) only allows updates through views
-- that map to a single underlying table with no GROUP BY,
-- aggregate functions, DISTINCT, or joins, since there is no
-- unambiguous way to translate the update back to base rows.
-- Example (will raise an error if executed):
-- UPDATE vw_student_enrollment_summary SET gpa = 4.0 WHERE student_id = 1;

-- Step 43: drop both views and recreate a single-table subset view
-- WITH CHECK OPTION, which blocks INSERT/UPDATE through the view
-- if the resulting row would fall outside the view's WHERE clause
DROP VIEW IF EXISTS vw_student_enrollment_summary;
DROP VIEW IF EXISTS vw_course_stats;

-- Recreate vw_course_stats (needed by later exercises)
CREATE OR REPLACE VIEW vw_course_stats AS
SELECT
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
            ELSE NULL
        END
    ),2) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;

-- Single-table subset view: only Computer Science students,
-- so it can support WITH CHECK OPTION
CREATE OR REPLACE VIEW vw_student_enrollment_summary AS
SELECT student_id, first_name, last_name, email, department_id, enrollment_year
FROM students
WHERE department_id = 1
WITH CHECK OPTION;

-- Any INSERT/UPDATE through this view that sets department_id
-- to something other than 1 will now be rejected by MySQL.


-- --------------------------------------------------------------
-- TASK 3: Stored Procedures and Transactions
-- --------------------------------------------------------------

-- Step 44: enroll a student in a course, guarding against duplicates
DELIMITER $$

DROP PROCEDURE IF EXISTS sp_enroll_student $$
CREATE PROCEDURE sp_enroll_student (
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_enrollment_date DATE
)
BEGIN
    DECLARE existing_count INT DEFAULT 0;

    SELECT COUNT(*) INTO existing_count
    FROM enrollments
    WHERE student_id = p_student_id AND course_id = p_course_id;

    IF existing_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Duplicate enrollment: this student is already enrolled in this course.';
    ELSE
        INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
        VALUES (p_student_id, p_course_id, p_enrollment_date, NULL);
    END IF;
END $$

DELIMITER ;

-- Table used to log department transfers (Step 45)
CREATE TABLE IF NOT EXISTS department_transfer_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    old_department_id INT,
    new_department_id INT,
    transfer_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Step 45: move a student to a new department, logging the change.
-- Both the UPDATE and the log INSERT happen inside one transaction
-- so that either both succeed or neither does.
DELIMITER $$

DROP PROCEDURE IF EXISTS sp_transfer_student $$
CREATE PROCEDURE sp_transfer_student (
    IN p_student_id INT,
    IN p_new_department_id INT
)
BEGIN
    DECLARE old_dept INT;

    -- If any statement in the block fails, roll back the whole transaction
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT department_id INTO old_dept
    FROM students WHERE student_id = p_student_id;

    UPDATE students
    SET department_id = p_new_department_id
    WHERE student_id = p_student_id;

    INSERT INTO department_transfer_log (student_id, old_department_id, new_department_id)
    VALUES (p_student_id, old_dept, p_new_department_id);

    COMMIT;
END $$

DELIMITER ;

-- Step 46: test the transaction with a deliberately invalid
-- department_id (e.g. 999, which has no matching row in
-- departments) - the FOREIGN KEY constraint on students.department_id
-- makes the UPDATE fail, the EXIT HANDLER rolls back, and the
-- student's department is left unchanged.
-- CALL sp_transfer_student(1, 999);

-- Step 47: SAVEPOINT demo - insert two enrollment records,
-- checkpoint after the first, deliberately fail the second,
-- then roll back only to the savepoint so the first insert survives.
START TRANSACTION;

INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
VALUES (2, 4, CURDATE(), NULL);

SAVEPOINT after_first_insert;

-- This second insert is deliberately invalid (course_id 9999
-- does not exist, violating the FOREIGN KEY constraint) to
-- simulate a failure partway through the transaction.
-- INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
-- VALUES (2, 9999, CURDATE(), NULL);

ROLLBACK TO SAVEPOINT after_first_insert;

COMMIT;

-- Verify: the first insert (student 2, course 4) persisted;
-- the failed second insert never took effect.
SELECT * FROM enrollments WHERE student_id = 2 AND course_id = 4;
