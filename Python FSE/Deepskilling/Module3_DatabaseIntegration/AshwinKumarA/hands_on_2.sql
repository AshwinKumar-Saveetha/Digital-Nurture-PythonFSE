-- ============================================================
-- Digital Nurture 5.0 - Module 3: Database Integration
-- HANDS-ON 2 [Beginner]
-- Writing SQL Queries - DML, Joins & Aggregations
-- Engine: MySQL 8.x
-- Prerequisite: run hands_on_1.sql first (creates college_db)
-- ============================================================

USE college_db;

-- --------------------------------------------------------------
-- TASK 1: Insert, Update and Delete Data
-- --------------------------------------------------------------

-- Step 15: load the sample data provided in the exercise book
INSERT INTO departments (dept_name, head_of_dept, budget) VALUES
('Computer Science','Dr. Ramesh Kumar',850000.00),
('Electronics','Dr. Priya Nair',620000.00),
('Mechanical','Dr. Suresh Iyer',540000.00),
('Civil','Dr. Ananya Sharma',430000.00);

INSERT INTO students (first_name,last_name,email,date_of_birth,department_id,enrollment_year) VALUES
('Arjun','Mehta','arjun.mehta@college.edu','2003-04-12',1,2022),
('Priya','Suresh','priya.suresh@college.edu','2003-07-25',1,2022),
('Rohan','Verma','rohan.verma@college.edu','2002-11-08',2,2021),
('Sneha','Patel','sneha.patel@college.edu','2004-01-30',3,2023),
('Vikram','Das','vikram.das@college.edu','2003-09-14',1,2022),
('Kavya','Menon','kavya.menon@college.edu','2002-05-17',2,2021),
('Aditya','Singh','aditya.singh@college.edu','2004-03-22',4,2023),
('Deepika','Rao','deepika.rao@college.edu','2003-08-09',1,2022);

INSERT INTO courses (course_name,course_code,credits,department_id) VALUES
('Data Structures & Algorithms','CS101',4,1),
('Database Management Systems','CS102',3,1),
('Object Oriented Programming','CS103',4,1),
('Circuit Theory','EC101',3,2),
('Thermodynamics','ME101',3,3);

INSERT INTO enrollments (student_id,course_id,enrollment_date,grade) VALUES
(1,1,'2022-07-01','A'),
(1,2,'2022-07-01','B'),
(2,1,'2022-07-01','B'),
(2,3,'2022-07-01','A'),
(3,4,'2021-07-01','A'),
(4,5,'2023-07-01',NULL),
(5,1,'2022-07-01','C'),
(5,2,'2022-07-01','A'),
(6,4,'2021-07-01','B'),
(7,5,'2023-07-01',NULL),
(8,1,'2022-07-01','A'),
(8,3,'2022-07-01','B');

INSERT INTO professors (prof_name,email,department_id,salary) VALUES
('Dr. Anand Krishnan','anand.k@college.edu',1,95000.00),
('Dr. Meena Pillai','meena.p@college.edu',1,88000.00),
('Dr. Sunil Rajan','sunil.r@college.edu',2,82000.00),
('Dr. Latha Gopal','latha.g@college.edu',3,79000.00),
('Dr. Kartik Bose','kartik.b@college.edu',4,76000.00);

-- Step 16: insert two additional students of our own choosing
INSERT INTO students (first_name,last_name,email,date_of_birth,department_id,enrollment_year) VALUES
('John','Doe','john.doe@college.edu','2003-01-01',1,2022),
('Jane','Smith','jane.smith@college.edu','2004-02-02',2,2023);

-- Step 17: update student 5's grade for course 1 from 'C' to 'B'
UPDATE enrollments SET grade = 'B'
WHERE student_id = 5 AND course_id = 1;

-- Step 18: preview rows before deleting (per the hint), then delete
-- enrollments that never received a grade
SELECT * FROM enrollments WHERE grade IS NULL;
DELETE FROM enrollments WHERE grade IS NULL;

-- Step 19: verify row counts
SELECT COUNT(*) AS total_students FROM students;      -- expect 10
SELECT COUNT(*) AS total_enrollments FROM enrollments; -- only non-NULL grades remain


-- --------------------------------------------------------------
-- TASK 2: Single-Table Queries and Filtering
-- --------------------------------------------------------------

-- Step 20: students enrolled in 2022, ordered alphabetically by last name
SELECT * FROM students WHERE enrollment_year = 2022 ORDER BY last_name;

-- Step 21: courses with more than 3 credits, highest credits first
SELECT * FROM courses WHERE credits > 3 ORDER BY credits DESC;

-- Step 22: professors earning between 80,000 and 95,000 (inclusive)
SELECT * FROM professors WHERE salary BETWEEN 80000 AND 95000;

-- Step 23: students whose email ends with '@college.edu'
SELECT * FROM students WHERE email LIKE '%@college.edu';

-- Step 24: count of students per enrollment year
SELECT enrollment_year, COUNT(*) AS total_students
FROM students
GROUP BY enrollment_year;


-- --------------------------------------------------------------
-- TASK 3: Multi-Table Joins
-- --------------------------------------------------------------

-- Step 25: each student's full name with their department name
SELECT CONCAT(s.first_name,' ',s.last_name) AS full_name, d.dept_name
FROM students s
JOIN departments d ON s.department_id = d.department_id;

-- Step 26: each enrollment with student name and course name
SELECT e.enrollment_id, CONCAT(s.first_name,' ',s.last_name) AS student_name, c.course_name
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id;

-- Step 27: students who are NOT enrolled in any course
SELECT s.*
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
WHERE e.enrollment_id IS NULL;

-- Step 28: every course with its enrollment count, including
-- courses that currently have zero students
SELECT c.course_name, COUNT(e.enrollment_id) AS enrolled_students
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name;

-- Step 29: each department with its professors and salaries,
-- including departments that currently have no professors
SELECT d.dept_name, p.prof_name, p.salary
FROM departments d
LEFT JOIN professors p ON d.department_id = p.department_id;


-- --------------------------------------------------------------
-- TASK 4: Aggregations and Grouping
-- --------------------------------------------------------------

-- Step 30: total enrollments per course
SELECT c.course_name, COUNT(*) AS enrollment_count
FROM courses c
JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_name;

-- Step 31: average professor salary per department, rounded to 2 dp
SELECT d.dept_name, ROUND(AVG(p.salary),2) AS avg_salary
FROM departments d
JOIN professors p ON d.department_id = p.department_id
GROUP BY d.dept_name;

-- Step 32: departments where the total budget exceeds 600,000
SELECT dept_name FROM departments WHERE budget > 600000;

-- Step 33: grade distribution for CS101
SELECT e.grade, COUNT(*) AS grade_count
FROM enrollments e
JOIN courses c ON e.course_id = c.course_id
WHERE c.course_code = 'CS101'
GROUP BY e.grade;

-- Step 34: departments with more than 2 students enrolled across
-- all their courses (HAVING filters on the aggregated result)
SELECT d.dept_name
FROM departments d
JOIN students s ON d.department_id = s.department_id
JOIN enrollments e ON s.student_id = e.student_id
GROUP BY d.dept_name
HAVING COUNT(*) > 2;
