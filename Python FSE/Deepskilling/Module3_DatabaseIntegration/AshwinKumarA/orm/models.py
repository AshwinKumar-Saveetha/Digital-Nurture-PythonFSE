"""
models.py - Hands-On 6, Task 1 (Steps 75-79)

Defines SQLAlchemy ORM model classes that mirror the college_db
relational schema from Hands-On 1, plus the is_active column and
CourseSchedule table that get added later in Hands-On 7's migration
history (Task 2, Steps 98-102).

Run this file directly to create all tables in a fresh database
(college_db_orm) via Base.metadata.create_all(engine):

    python models.py
"""

import os
from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey,
    Date, DateTime, Numeric, Boolean, Time
)
from sqlalchemy.orm import declarative_base, relationship

# --------------------------------------------------------------
# Database connection
# --------------------------------------------------------------
# Assumption: connection details are read from an environment
# variable so the same code works for any user/host/password
# without hard-coding credentials in source control. Falls back to
# a sensible local default matching the exercise book's schema
# (college_db_orm) if the variable is not set.
DATABASE_URL = os.environ.get(
    "COLLEGE_DB_ORM_URL",
    "mysql+mysqlconnector://root:password@localhost:3306/college_db_orm",
)

# echo=True prints every SQL statement issued - very useful for
# spotting the N+1 problem in Hands-On 6, Task 2/3.
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()


class Department(Base):
    """Mirrors the departments table from Hands-On 1."""
    __tablename__ = 'departments'

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name = Column(String(100), nullable=False)
    hod_name = Column(String(100))
    budget = Column(Numeric(12, 2))

    students = relationship('Student', back_populates='department')
    courses = relationship('Course', back_populates='department')
    professors = relationship('Professor', back_populates='department')


class Student(Base):
    """Mirrors the students table, plus is_active added by the
    add_is_active migration (Hands-On 7, Task 2)."""
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    date_of_birth = Column(Date)
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    enrollment_year = Column(Integer)
    is_active = Column(Boolean, default=True)

    department = relationship('Department', back_populates='students')
    enrollments = relationship('Enrollment', back_populates='student')


class Course(Base):
    """Mirrors the courses table."""
    __tablename__ = 'courses'

    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(150), nullable=False)
    course_code = Column(String(20), unique=True)
    credits = Column(Integer)
    department_id = Column(Integer, ForeignKey('departments.department_id'))

    department = relationship('Department', back_populates='courses')
    enrollments = relationship('Enrollment', back_populates='course')
    schedules = relationship('CourseSchedule', back_populates='course')


class Enrollment(Base):
    """Mirrors the enrollments table. Many-to-one to both Student
    and Course."""
    __tablename__ = 'enrollments'

    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    course_id = Column(Integer, ForeignKey('courses.course_id'))
    enrollment_date = Column(Date)
    grade = Column(String(2))

    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')


class Professor(Base):
    """Mirrors the professors table."""
    __tablename__ = 'professors'

    professor_id = Column(Integer, primary_key=True, autoincrement=True)
    prof_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    salary = Column(Numeric(10, 2))

    department = relationship('Department', back_populates='professors')


class CourseSchedule(Base):
    """Added by the add_course_schedule migration (Hands-On 7,
    Task 2, Step 102)."""
    __tablename__ = 'course_schedules'

    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'))
    day_of_week = Column(String(20))
    start_time = Column(Time)
    end_time = Column(Time)

    course = relationship('Course', back_populates='schedules')


if __name__ == '__main__':
    # Step 79: auto-create every table defined above in a fresh
    # database. In a real project you would normally let Alembic
    # (see ../migrations/) manage schema creation instead of calling
    # create_all() directly - this is provided so models.py can also
    # be run standalone, as the exercise book instructs.
    Base.metadata.create_all(engine)
    print("All tables created successfully in college_db_orm.")
