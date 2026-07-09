from typing import Optional

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import create_tables, get_db
from models import Course, Department, Enrollment, Student
from schemas import (
    CourseCreate,
    CourseResponse,
    CourseUpdate,
    EnrollmentCreate,
    EnrollmentResponse,
    EnrollmentUpdate,
    StudentCreate,
    StudentResponse,
    StudentUpdate,
)


app = FastAPI(
    title="Course Management API",
    description="FastAPI Course Management API with Courses, Students, Enrollments, CRUD operations, Background Tasks and OpenAPI documentation.",
    version="1.0",
    contact={
        "name": "Ashwin Kumar A",
        "email": "ashwin@example.com",
    },
)


@app.on_event("startup")
async def startup_event() -> None:
    await create_tables()


def send_confirmation_email(student_email: str):
    print(f"Sending confirmation to {student_email}")


@app.get("/", tags=["Root"])
async def root():
    return {"message": "API running"}


async def ensure_department(db: AsyncSession, department_id: int):
    department = await db.get(Department, department_id)

    if department is None:
        department = Department(
            id=department_id,
            name=f"Department {department_id}",
        )
        db.add(department)
        await db.flush()

    return department


@app.post(
    "/api/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
    summary="Create a new course",
    response_description="The created course details",
)
async def create_course(
    course: CourseCreate,
    db: AsyncSession = Depends(get_db),
):
    await ensure_department(db, course.department_id)

    new_course = Course(
        name=course.name,
        code=course.code,
        credits=course.credits,
        department_id=course.department_id,
    )

    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)

    return new_course


@app.get("/api/courses/", response_model=list[CourseResponse], tags=["Courses"])
async def get_courses(
    skip: int = 0,
    limit: int = 10,
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Course)

    if department_id is not None:
        query = query.where(Course.department_id == department_id)

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


@app.get("/api/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    course = await db.get(Course, course_id)

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    return course


@app.put("/api/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def update_course(
    course_id: int,
    course_update: CourseUpdate,
    db: AsyncSession = Depends(get_db),
):
    course = await db.get(Course, course_id)

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    update_data = course_update.model_dump(exclude_unset=True)

    if "department_id" in update_data:
        await ensure_department(db, update_data["department_id"])

    for field, value in update_data.items():
        setattr(course, field, value)

    await db.commit()
    await db.refresh(course)

    return course


@app.delete(
    "/api/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Courses"],
)
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    course = await db.get(Course, course_id)

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    await db.delete(course)
    await db.commit()


@app.get(
    "/api/courses/{course_id}/students/",
    response_model=list[StudentResponse],
    tags=["Courses"],
)
async def get_students_by_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    course = await db.get(Course, course_id)

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    query = (
        select(Student)
        .join(Enrollment, Student.id == Enrollment.student_id)
        .where(Enrollment.course_id == course_id)
    )

    result = await db.execute(query)
    return result.scalars().all()


@app.post(
    "/api/students/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
)
async def create_student(
    student: StudentCreate,
    db: AsyncSession = Depends(get_db),
):
    await ensure_department(db, student.department_id)

    new_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
        department_id=student.department_id,
        enrollment_year=student.enrollment_year,
    )

    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)

    return new_student


@app.get("/api/students/", response_model=list[StudentResponse], tags=["Students"])
async def get_students(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Student))
    return result.scalars().all()


@app.get("/api/students/{student_id}", response_model=StudentResponse, tags=["Students"])
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    student = await db.get(Student, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@app.put("/api/students/{student_id}", response_model=StudentResponse, tags=["Students"])
async def update_student(
    student_id: int,
    student_update: StudentUpdate,
    db: AsyncSession = Depends(get_db),
):
    student = await db.get(Student, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = student_update.model_dump(exclude_unset=True)

    if "department_id" in update_data:
        await ensure_department(db, update_data["department_id"])

    for field, value in update_data.items():
        setattr(student, field, value)

    await db.commit()
    await db.refresh(student)

    return student


@app.delete(
    "/api/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Students"],
)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    student = await db.get(Student, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    await db.delete(student)
    await db.commit()


@app.post(
    "/api/enrollments/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"],
)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    student = await db.get(Student, enrollment.student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    course = await db.get(Course, enrollment.course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    new_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        enrollment_date=enrollment.enrollment_date,
        grade=enrollment.grade,
    )

    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)

    background_tasks.add_task(send_confirmation_email, student.email)

    return new_enrollment


@app.get(
    "/api/enrollments/",
    response_model=list[EnrollmentResponse],
    tags=["Enrollments"],
)
async def get_enrollments(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Enrollment))
    return result.scalars().all()


@app.get(
    "/api/enrollments/{enrollment_id}",
    response_model=EnrollmentResponse,
    tags=["Enrollments"],
)
async def get_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db),
):
    enrollment = await db.get(Enrollment, enrollment_id)

    if enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    return enrollment


@app.put(
    "/api/enrollments/{enrollment_id}",
    response_model=EnrollmentResponse,
    tags=["Enrollments"],
)
async def update_enrollment(
    enrollment_id: int,
    enrollment_update: EnrollmentUpdate,
    db: AsyncSession = Depends(get_db),
):
    enrollment = await db.get(Enrollment, enrollment_id)

    if enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    update_data = enrollment_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(enrollment, field, value)

    await db.commit()
    await db.refresh(enrollment)

    return enrollment


@app.delete(
    "/api/enrollments/{enrollment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Enrollments"],
)
async def delete_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db),
):
    enrollment = await db.get(Enrollment, enrollment_id)

    if enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    await db.delete(enrollment)
    await db.commit()