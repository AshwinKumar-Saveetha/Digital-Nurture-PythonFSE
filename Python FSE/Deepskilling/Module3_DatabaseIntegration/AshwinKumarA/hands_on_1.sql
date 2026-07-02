-- ============================================================
-- Digital Nurture 5.0 - Module 3: Database Integration
-- HANDS-ON 1 [Beginner]
-- Schema Design & Core SQL - DDL and Normalisation
-- Engine: MySQL 8.x
-- ============================================================

-- --------------------------------------------------------------
-- TASK 1: Create the Database and Tables
-- Goal: Practise DDL by creating the full college_db schema
-- with proper constraints (PK, FK, UNIQUE, NOT NULL).
-- --------------------------------------------------------------

DROP DATABASE IF EXISTS college_db;
CREATE DATABASE college_db;
USE college_db;

-- departments must be created first, since students, courses and
-- professors all reference it via FOREIGN KEY.
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

-- Verify with: DESCRIBE departments; DESCRIBE students; etc.
-- Expected Outcome: all 5 tables created with no errors.


-- --------------------------------------------------------------
-- TASK 2: Verify Normalisation (1NF, 2NF, 3NF)
-- Goal: Confirm the schema is normalised and document why.
-- --------------------------------------------------------------

-- 1NF (Atomicity):
-- Every column in every table holds a single, atomic value
-- (e.g. first_name and last_name are stored separately, rather
-- than one combined "name" field; email is a single value, not
-- a list). A hypothetical violation would be storing multiple
-- phone numbers in one comma-separated column such as
-- '9876543210,9123456780' - that would break 1NF because the
-- column would no longer hold a single atomic value.

-- 2NF (Full functional dependency on the whole key):
-- Every table here uses a single-column surrogate primary key
-- (student_id, course_id, etc.), so partial-key dependency is
-- not possible. The one table with a natural composite candidate
-- key is enrollments (student_id + course_id): every non-key
-- column (enrollment_date, grade) depends on the *combination*
-- of student_id and course_id together, not on just one of them,
-- so 2NF holds.

-- 3NF (No transitive dependency):
-- A transitive dependency exists when column C depends on column
-- B, which depends on the primary key A, rather than directly on
-- A. If we stored dept_name directly inside the students table,
-- dept_name would depend on department_id, and department_id
-- depends on student_id - a transitive dependency, violating 3NF.
-- Instead, department details are kept in their own departments
-- table and referenced only via department_id (a foreign key),
-- so students, courses, professors and enrollments all satisfy 3NF.


-- --------------------------------------------------------------
-- TASK 3: Alter and Extend the Schema
-- Goal: Use ALTER TABLE to safely extend the schema without
-- losing existing data.
-- --------------------------------------------------------------

-- Step 10: add phone_number to students
ALTER TABLE students ADD phone_number VARCHAR(15);

-- Step 11: add max_seats to courses with a sensible default
ALTER TABLE courses ADD max_seats INT DEFAULT 60;

-- Step 12: enforce a valid grade value or NULL (MySQL 8+ enforces
-- CHECK constraints; older MySQL parses but ignores them)
ALTER TABLE enrollments
ADD CONSTRAINT chk_grade
CHECK (grade IN ('A','B','C','D','F') OR grade IS NULL);

-- Step 13: rename hod_name -> head_of_dept (MySQL uses CHANGE,
-- Postgres would use ALTER COLUMN ... RENAME TO)
ALTER TABLE departments
CHANGE hod_name head_of_dept VARCHAR(100);

-- Step 14: simulate a schema rollback by dropping the column
-- we just added
ALTER TABLE students DROP COLUMN phone_number;

-- Verify all changes:
-- SELECT * FROM INFORMATION_SCHEMA.COLUMNS
-- WHERE TABLE_SCHEMA = 'college_db';

-- Expected Outcome: final schema = original + courses.max_seats
-- + departments.head_of_dept (renamed from hod_name).
