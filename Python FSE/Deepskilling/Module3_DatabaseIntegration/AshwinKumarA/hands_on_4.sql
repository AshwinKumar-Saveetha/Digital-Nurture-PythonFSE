-- ============================================================
-- Digital Nurture 5.0 - Module 3: Database Integration
-- HANDS-ON 4 [Intermediate]
-- Query Optimisation - Indexes, EXPLAIN & the N+1 Problem
-- Engine: MySQL 8.x
-- Prerequisite: run hands_on_1.sql, hands_on_2.sql, hands_on_3.sql first
-- ============================================================

USE college_db;

-- --------------------------------------------------------------
-- TASK 1: Baseline Performance - No Indexes
-- --------------------------------------------------------------

-- Step 48: baseline EXPLAIN before any optimisation
EXPLAIN FORMAT=JSON
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

-- Step 49-50: SAMPLE baseline observations (actual numbers will
-- vary with your data/MySQL version - re-run and paste your own
-- output here as documentation):
--
--   table: s (students)  -> type: ALL (full table scan),
--                            rows examined ~ 10 (no index on enrollment_year yet)
--   table: e (enrollments) -> type: ALL (full table scan)
--   table: c (courses)     -> type: eq_ref (uses PRIMARY KEY, already fast)
--
-- On a small sample table a full scan ("ALL") is not necessarily
-- slow, but it does not scale - as the students/enrollments
-- tables grow to thousands/millions of rows, these full scans
-- become the main cost of the query. That is exactly what
-- Task 2 addresses.


-- --------------------------------------------------------------
-- TASK 2: Add Indexes and Compare Plans
-- --------------------------------------------------------------

-- Step 51: B-Tree index on students.enrollment_year (equality
-- filter column - put it first for composite indexes generally,
-- and it's the only filter column here)
CREATE INDEX idx_students_enrollment_year ON students(enrollment_year);

-- Step 52: composite UNIQUE index - also prevents duplicate
-- (student_id, course_id) enrollment rows going forward
CREATE UNIQUE INDEX idx_enrollments_student_course
ON enrollments(student_id, course_id);

-- Step 53: index to speed up course_code lookups (already UNIQUE
-- from the DDL, but demonstrating an explicit secondary index
-- is still a valid pattern for non-unique lookup columns)
CREATE INDEX idx_courses_course_code ON courses(course_code);

-- Step 54: re-run EXPLAIN and compare to the baseline
EXPLAIN FORMAT=JSON
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

-- Expected change: the "students" table access type should move
-- from ALL (full table scan) to ref/range, using
-- idx_students_enrollment_year - i.e. Seq Scan -> Index Scan.

-- Step 55: MySQL 8.x does NOT support PostgreSQL-style partial
-- indexes (an index that only covers rows matching a WHERE
-- condition). ASSUMPTION/DOCUMENTED WORKAROUND: since this
-- project standardises on MySQL 8.x, we approximate the same
-- intent - a fast lookup for "enrollments with no grade yet" -
-- with a regular composite index that leads with the column we
-- filter on. This indexes all rows (not just grade IS NULL rows
-- like a true partial index would), but still gives MySQL an
-- efficient access path for this query pattern:
CREATE INDEX idx_enrollments_student_grade ON enrollments(student_id, grade);

-- Query that benefits from the index above:
SELECT * FROM enrollments WHERE student_id = 4 AND grade IS NULL;

-- If you are running this exercise against PostgreSQL instead,
-- the true partial index would be:
-- CREATE INDEX idx_enrollments_pending_grade
-- ON enrollments(student_id) WHERE grade IS NULL;


-- --------------------------------------------------------------
-- TASK 3: Identify and Fix the N+1 Problem
-- --------------------------------------------------------------
-- Steps 56-59 ask for a Python demonstration of the N+1 problem,
-- which is not expressible in plain SQL. The runnable script for
-- this task lives at orm/n_plus_one_demo.py (documented assumption:
-- since the required project layout does not list a dedicated
-- "scripts" folder, this demo script is kept alongside the other
-- Python/SQLAlchemy code in orm/, and is referenced here).
--
-- Summary of what orm/n_plus_one_demo.py demonstrates:
--   1. "Naive" version: SELECT * FROM enrollments (1 query),
--      then loop over each row issuing a separate
--      SELECT * FROM students WHERE student_id = ? (N queries).
--      Total = 1 + N queries (13 with the 12 sample enrollments).
--   2. "Optimised" version: a single JOIN query that retrieves
--      all enrollment rows together with student names in one
--      round trip (1 query total).
--   3. Both versions are timed with Python's time module and the
--      query counts / durations are printed for comparison.
--
-- Step 59 answer (documented here): in a real application with
-- 10,000 enrollments, the naive N+1 version would issue
-- 1 + 10,000 = 10,001 queries instead of 1 - 10,000 avoidable
-- extra round trips to the database.
