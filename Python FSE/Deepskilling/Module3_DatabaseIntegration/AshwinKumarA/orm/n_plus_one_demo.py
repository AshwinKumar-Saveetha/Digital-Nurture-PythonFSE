"""
n_plus_one_demo.py - Hands-On 4, Task 3 (Steps 56-59)

Referenced from ../hands_on_4.sql. A standalone, self-contained
demonstration of the N+1 query problem using plain SQLAlchemy Core
(no ORM session needed), so query counts are easy to see and count
by hand.

  Version 1 (naive):     1 query to fetch all enrollments, then 1
                          extra query PER ROW to fetch the related
                          student's name  ->  1 + N queries.
  Version 2 (optimised):  a single JOIN query returns every
                          enrollment with its student name already
                          attached -> 1 query total.

With the 12 sample enrollments from hands_on_2.sql (12 remain after
hands_on_2.sql's DELETE ... WHERE grade IS NULL removes 2 of the
original 14), Version 1 prints "13 queries executed" and Version 2
prints "1 query executed" - matching the exercise book's Expected
Outcome for Hands-On 4, Task 3.

Run with:
    python n_plus_one_demo.py
"""

import time
from sqlalchemy import text
from models import engine

QUERY_COUNT = 0


def run_query(connection, sql, params=None):
    """Small helper that executes a query and increments a global
    counter, so we can print an exact count at the end - this
    mirrors what you would otherwise read off the SQLAlchemy
    echo=True log."""
    global QUERY_COUNT
    QUERY_COUNT += 1
    return connection.execute(text(sql), params or {})


def demo_naive_n_plus_one():
    """Version 1: 1 query for all enrollments, then 1 query PER
    enrollment to fetch the student's name - the N+1 anti-pattern."""
    global QUERY_COUNT
    QUERY_COUNT = 0
    start = time.time()

    with engine.connect() as connection:
        enrollments = run_query(
            connection, "SELECT enrollment_id, student_id, course_id FROM enrollments"
        ).fetchall()

        results = []
        for row in enrollments:
            student = run_query(
                connection,
                "SELECT first_name, last_name FROM students WHERE student_id = :sid",
                {"sid": row.student_id},
            ).fetchone()
            if student:
                results.append(f"{student.first_name} {student.last_name}")

    elapsed = time.time() - start
    print(f"Naive (N+1) version: {QUERY_COUNT} queries executed in {elapsed:.4f}s")
    return results, QUERY_COUNT


def demo_optimised_join():
    """Version 2: a single JOIN query eliminates the N+1 pattern."""
    global QUERY_COUNT
    QUERY_COUNT = 0
    start = time.time()

    with engine.connect() as connection:
        rows = run_query(
            connection,
            """
            SELECT e.enrollment_id, s.first_name, s.last_name
            FROM enrollments e
            JOIN students s ON s.student_id = e.student_id
            """,
        ).fetchall()
        results = [f"{row.first_name} {row.last_name}" for row in rows]

    elapsed = time.time() - start
    print(f"Optimised (JOIN) version: {QUERY_COUNT} query executed in {elapsed:.4f}s")
    return results, QUERY_COUNT


if __name__ == '__main__':
    naive_results, naive_count = demo_naive_n_plus_one()
    optimised_results, optimised_count = demo_optimised_join()

    print(f"\nBoth versions returned identical data: {naive_results == optimised_results}")
    print(f"Query round-trips saved: {naive_count - optimised_count}")
