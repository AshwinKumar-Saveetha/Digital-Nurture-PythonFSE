"""
crud.py - Hands-On 6, Task 2 (Steps 80-86) and Task 3 (Steps 87-91)

OBSERVATION FOR TASK 3 (query-count comparison):
  Naive/lazy-loaded read (Step 84): 1 query to fetch all enrollments,
  then 1 extra query for EACH related student and EACH related
  course accessed in the loop - classic N+1. With 4 enrollments that
  is 1 + 4 (students) + 4 (courses) = 9 extra lookups on top of the
  first query in the worst case (SQLAlchemy's identity map may cache
  repeats within a session, but a fresh session shows the full N+1
  pattern).

  joinedload() read (Step 88): exactly 1 query, using SQL LEFT OUTER
  JOINs to pull enrollments + students + courses together in a
  single round trip.

Run with:
    python crud.py
"""

from sqlalchemy.orm import sessionmaker, joinedload
from models import engine, Department, Student, Course, Enrollment

# Step 80: open a session bound to the engine defined in models.py
Session = sessionmaker(bind=engine)
session = Session()

# --------------------------------------------------------------
# Step 81: INSERT 3 departments and 5 students
# --------------------------------------------------------------
dept_cs = Department(dept_name='Computer Science')
dept_math = Department(dept_name='Mathematics')
dept_phy = Department(dept_name='Physics')
session.add_all([dept_cs, dept_math, dept_phy])
session.commit()

student1 = Student(first_name='Alice', last_name='Anderson', email='alice@test.com',
                    enrollment_year=2024, department=dept_cs)
student2 = Student(first_name='Bob', last_name='Brown', email='bob@test.com',
                    enrollment_year=2024, department=dept_cs)
student3 = Student(first_name='Charlie', last_name='Clark', email='charlie@test.com',
                    enrollment_year=2023, department=dept_math)
student4 = Student(first_name='Diana', last_name='Diaz', email='diana@test.com',
                    enrollment_year=2025, department=dept_phy)
student5 = Student(first_name='Eve', last_name='Evans', email='eve@test.com',
                    enrollment_year=2024, department=dept_cs)
session.add_all([student1, student2, student3, student4, student5])
session.commit()

# --------------------------------------------------------------
# Step 82: INSERT 3 courses and 4 enrollments
# --------------------------------------------------------------
course1 = Course(course_name='Database Systems', course_code='DB201', credits=4)
course2 = Course(course_name='Calculus', course_code='MA101', credits=3)
course3 = Course(course_name='Quantum Mechanics', course_code='PH301', credits=4)
session.add_all([course1, course2, course3])
session.commit()

enr1 = Enrollment(student=student1, course=course1)
enr2 = Enrollment(student=student2, course=course1)
enr3 = Enrollment(student=student3, course=course2)
enr4 = Enrollment(student=student4, course=course3)
session.add_all([enr1, enr2, enr3, enr4])
session.commit()

print("\n--- Data Inserted Successfully ---\n")

# --------------------------------------------------------------
# Step 83: READ all students in 'Computer Science'
# --------------------------------------------------------------
print("--- CS Students ---")
cs_students = (
    session.query(Student)
    .join(Department)
    .filter(Department.dept_name == 'Computer Science')
    .all()
)
for s in cs_students:
    print(f"{s.first_name} {s.last_name}")

# --------------------------------------------------------------
# Step 84: READ all enrollments (demonstrates the N+1 problem -
# watch the SQL log printed by echo=True in models.py: one extra
# SELECT fires for each .student and .course access below)
# --------------------------------------------------------------
print("\n--- All Enrollments (N+1 Issue) ---")
all_enrollments = session.query(Enrollment).all()
for e in all_enrollments:
    print(f"{e.student.first_name} {e.student.last_name} is enrolled in {e.course.course_name}")

# --------------------------------------------------------------
# Step 85: UPDATE a student's enrollment_year
# --------------------------------------------------------------
student_to_update = session.query(Student).filter(Student.email == 'alice@test.com').first()
if student_to_update:
    student_to_update.enrollment_year = 2026
    session.commit()
    print("\n--- Updated Alice's enrollment_year ---")

# --------------------------------------------------------------
# Step 86: DELETE an enrollment record
# --------------------------------------------------------------
enr_to_delete = session.query(Enrollment).filter(Enrollment.student_id == student2.student_id).first()
if enr_to_delete:
    session.delete(enr_to_delete)
    session.commit()
    print("--- Deleted Bob's enrollment ---\n")

# --------------------------------------------------------------
# Task 3 (Steps 87-90): fix the N+1 problem with eager loading.
# joinedload() rewrites the query to use SQL JOINs so student and
# course data comes back in the SAME query as the enrollments,
# instead of one extra query per related row.
# --------------------------------------------------------------
print("--- Optimised Enrollments (Fixing N+1) ---")
optimized_enrollments = (
    session.query(Enrollment)
    .options(joinedload(Enrollment.student), joinedload(Enrollment.course))
    .all()
)
for e in optimized_enrollments:
    print(f"{e.student.first_name} {e.student.last_name} is enrolled in {e.course.course_name}")

session.close()
