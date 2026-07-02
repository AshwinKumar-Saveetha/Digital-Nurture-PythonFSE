-- Digital Nurture 5.0 - Module 3
-- Database Integration
-- Hands-On 1 to Hands-On 4 (MySQL 8.x)


DROP DATABASE IF EXISTS college_db;
CREATE DATABASE college_db;
USE college_db;

-- =========================
-- HANDS-ON 1
-- =========================

CREATE TABLE departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(100) NOT NULL,
    hod_name VARCHAR(100),
    budget DECIMAL(12,2)
);

CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    department_id INT,
    enrollment_year INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(20) UNIQUE,
    credits INT,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    grade CHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE professors (
    professor_id INT PRIMARY KEY AUTO_INCREMENT,
    prof_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_id INT,
    salary DECIMAL(10,2),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Normalization Analysis
-- 1NF: All attributes contain atomic values.
-- 2NF: All non-key attributes depend on the whole primary key.
-- 3NF: No transitive dependency exists.
-- Department details are stored separately.
-- Enrollments satisfy 3NF.

ALTER TABLE students ADD phone_number VARCHAR(15);
ALTER TABLE courses ADD max_seats INT DEFAULT 60;
ALTER TABLE enrollments
ADD CONSTRAINT chk_grade
CHECK (grade IN ('A','B','C','D','F') OR grade IS NULL);

ALTER TABLE departments
CHANGE hod_name head_of_dept VARCHAR(100);

ALTER TABLE students DROP COLUMN phone_number;

-- =========================
-- HANDS-ON 2
-- =========================

INSERT INTO departments (dept_name, head_of_dept, budget) VALUES
('Computer Science','Dr. Ramesh Kumar',850000.00),
('Electronics','Dr. Priya Nair',620000.00),
('Mechanical','Dr. Suresh Iyer',540000.00),
('Civil','Dr. Ananya Sharma',430000.00);

INSERT INTO students(first_name,last_name,email,date_of_birth,department_id,enrollment_year) VALUES
('Arjun','Mehta','arjun.mehta@college.edu','2003-04-12',1,2022),
('Priya','Suresh','priya.suresh@college.edu','2003-07-25',1,2022),
('Rohan','Verma','rohan.verma@college.edu','2002-11-08',2,2021),
('Sneha','Patel','sneha.patel@college.edu','2004-01-30',3,2023),
('Vikram','Das','vikram.das@college.edu','2003-09-14',1,2022),
('Kavya','Menon','kavya.menon@college.edu','2002-05-17',2,2021),
('Aditya','Singh','aditya.singh@college.edu','2004-03-22',4,2023),
('Deepika','Rao','deepika.rao@college.edu','2003-08-09',1,2022);

INSERT INTO courses(course_name,course_code,credits,department_id) VALUES
('Data Structures & Algorithms','CS101',4,1),
('Database Management Systems','CS102',3,1),
('Object Oriented Programming','CS103',4,1),
('Circuit Theory','EC101',3,2),
('Thermodynamics','ME101',3,3);

INSERT INTO enrollments(student_id,course_id,enrollment_date,grade) VALUES
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

INSERT INTO professors(prof_name,email,department_id,salary) VALUES
('Dr. Anand Krishnan','anand.k@college.edu',1,95000),
('Dr. Meena Pillai','meena.p@college.edu',1,88000),
('Dr. Sunil Rajan','sunil.r@college.edu',2,82000),
('Dr. Latha Gopal','latha.g@college.edu',3,79000),
('Dr. Kartik Bose','kartik.b@college.edu',4,76000);

INSERT INTO students(first_name,last_name,email,date_of_birth,department_id,enrollment_year)
VALUES
('John','Doe','john.doe@college.edu','2003-01-01',1,2022),
('Jane','Smith','jane.smith@college.edu','2004-02-02',2,2023);

UPDATE enrollments SET grade='B'
WHERE student_id=5 AND course_id=1;

DELETE FROM enrollments WHERE grade IS NULL;

SELECT * FROM students WHERE enrollment_year=2022 ORDER BY last_name;
SELECT * FROM courses WHERE credits>3 ORDER BY credits DESC;
SELECT * FROM professors WHERE salary BETWEEN 80000 AND 95000;
SELECT * FROM students WHERE email LIKE '%@college.edu';
SELECT enrollment_year,COUNT(*) total_students FROM students GROUP BY enrollment_year;

SELECT CONCAT(s.first_name,' ',s.last_name) full_name,d.dept_name
FROM students s JOIN departments d ON s.department_id=d.department_id;

SELECT e.enrollment_id,CONCAT(s.first_name,' ',s.last_name) student_name,c.course_name
FROM enrollments e
JOIN students s ON e.student_id=s.student_id
JOIN courses c ON e.course_id=c.course_id;

SELECT s.*
FROM students s
LEFT JOIN enrollments e ON s.student_id=e.student_id
WHERE e.enrollment_id IS NULL;

SELECT c.course_name,COUNT(e.enrollment_id) enrolled_students
FROM courses c
LEFT JOIN enrollments e ON c.course_id=e.course_id
GROUP BY c.course_id,c.course_name;

SELECT d.dept_name,p.prof_name,p.salary
FROM departments d
LEFT JOIN professors p ON d.department_id=p.department_id;

SELECT c.course_name,COUNT(*) enrollment_count
FROM courses c JOIN enrollments e ON c.course_id=e.course_id
GROUP BY c.course_name;

SELECT d.dept_name,ROUND(AVG(p.salary),2) avg_salary
FROM departments d
JOIN professors p ON d.department_id=p.department_id
GROUP BY d.dept_name;

SELECT dept_name FROM departments WHERE budget>600000;

SELECT e.grade,COUNT(*) grade_count
FROM enrollments e
JOIN courses c ON e.course_id=c.course_id
WHERE c.course_code='CS101'
GROUP BY e.grade;

SELECT d.dept_name
FROM departments d
JOIN students s ON d.department_id=s.department_id
JOIN enrollments e ON s.student_id=e.student_id
GROUP BY d.dept_name
HAVING COUNT(*)>2;

-- =========================
-- HANDS-ON 3 & 4
-- (Representative correct solutions)
-- =========================

SELECT p.*
FROM professors p
WHERE salary=(
SELECT MAX(salary)
FROM professors p2
WHERE p2.department_id=p.department_id);

CREATE INDEX idx_students_enrollment_year ON students(enrollment_year);
CREATE UNIQUE INDEX idx_enrollments_student_course
ON enrollments(student_id,course_id);
CREATE INDEX idx_courses_course_code ON courses(course_code);


SELECT s.first_name,s.last_name,c.course_name
FROM enrollments e
JOIN students s ON s.student_id=e.student_id
JOIN courses c ON c.course_id=e.course_id
WHERE s.enrollment_year=2022;
