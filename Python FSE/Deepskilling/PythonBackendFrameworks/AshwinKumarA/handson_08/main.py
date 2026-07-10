from typing import Optional

from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import create_tables, get_db
from models import Course, Department, Enrollment, Student
from schemas import (
    CourseCreate,
    CourseListEnvelope,
    CoursePatch,
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
    description=(
        "FastAPI Course Management API with RESTful naming, API versioning, "
        "pagination, filtering, standardised errors, Background Tasks, "
        "and OpenAPI documentation."
    ),
    version="1.0",
    contact={
        "name": "Ashwin Kumar A",
        "email": "ashwin@example.com",
    },
)


# API versioning note:
# URL versioning, such as /api/v1/courses/, is simple, explicit, and easy
# to test in browsers and API clients.
# Header-based versioning keeps URLs cleaner but requires clients to send
# a version in a header such as:
# Accept: application/vnd.api+json;version=1


@app.on_event("startup")
async def startup_event() -> None:
    await create_tables()


def send_confirmation_email(student_email: str) -> None:
    print(f"Sending confirmation to {student_email}")


def error_response(
    code: str,
    message: str,
    field: Optional[str] = None,
) -> dict:
    return {
        "error": {
            "code": code,
            "message": message,
            "field": field,
        }
    }


def not_found(resource: str, resource_id: int) -> None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "code": "NOT_FOUND",
            "message": f"{resource} with id {resource_id} does not exist",
            "field": None,
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    if isinstance(exc.detail, dict) and "code" in exc.detail:
        content = {"error": exc.detail}
    else:
        content = error_response(
            code="HTTP_ERROR",
            message=str(exc.detail),
            field=None,
        )

    return JSONResponse(
        status_code=exc.status_code,
        content=content,
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors = exc.errors()
    first_error = errors[0] if errors else {}

    location = first_error.get("loc", [])
    field = str(location[-1]) if location else None
    message = first_error.get("msg", "Request validation failed")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(
            code="VALIDATION_ERROR",
            message=message,
            field=field,
        ),
    )


@app.get("/", tags=["Root"])
async def root():
    return {"message": "API running"}


async def ensure_department(
    db: AsyncSession,
    department_id: int,
):
    department = await db.get(Department, department_id)

    if department is None:
        department = Department(
            id=department_id,
            name=f"Department {department_id}",
        )
        db.add(department)
        await db.flush()

    return department


# ==================================================
# COURSES
# ==================================================


@app.post(
    "/api/v1/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
    summary="Create a new course",
    response_description="The created course details",
)
async def create_course(
    course: CourseCreate,
    response: Response,
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

    response.headers["Location"] = f"/api/v1/courses/{new_course.id}/"

    return new_course


@app.get(
    "/api/v1/courses/",
    response_model=CourseListEnvelope,
    tags=["Courses"],
)
async def get_courses(
    request: Request,
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "BAD_REQUEST",
                "message": "page must be greater than or equal to 1",
                "field": "page",
            },
        )

    if page_size < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "BAD_REQUEST",
                "message": "page_size must be greater than or equal to 1",
                "field": "page_size",
            },
        )

    query = select(Course)
    count_query = select(func.count()).select_from(Course)

    if search:
        search_pattern = f"%{search}%"
        search_filter = or_(
            Course.name.ilike(search_pattern),
            Course.code.ilike(search_pattern),
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    courses = result.scalars().all()

    base_url = str(request.url.replace(query=""))
    search_part = f"&search={search}" if search else ""

    next_url = None
    if offset + page_size < total:
        next_url = (
            f"{base_url}?page={page + 1}"
            f"&page_size={page_size}{search_part}"
        )

    previous_url = None
    if page > 1:
        previous_url = (
            f"{base_url}?page={page - 1}"
            f"&page_size={page_size}{search_part}"
        )

    return {
        "count": total,
        "next": next_url,
        "previous": previous_url,
        "results": courses,
    }


@app.get(
    "/api/v1/courses/{course_id}/",
    response_model=CourseResponse,
    tags=["Courses"],
)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    course = await db.get(Course, course_id)

    if course is None:
        not_found("Course", course_id)

    return course


@app.put(
    "/api/v1/courses/{course_id}/",
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
    tags=["Courses"],
)
async def update_course(
    course_id: int,
    course_update: CourseUpdate,
    db: AsyncSession = Depends(get_db),
):
    course = await db.get(Course, course_id)

    if course is None:
        not_found("Course", course_id)

    await ensure_department(db, course_update.department_id)

    course.name = course_update.name
    course.code = course_update.code
    course.credits = course_update.credits
    course.department_id = course_update.department_id

    await db.commit()
    await db.refresh(course)

    return course


@app.patch(
    "/api/v1/courses/{course_id}/",
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
    tags=["Courses"],
)
async def patch_course(
    course_id: int,
    course_patch: CoursePatch,
    db: AsyncSession = Depends(get_db),
):
    course = await db.get(Course, course_id)

    if course is None:
        not_found("Course", course_id)

    update_data = course_patch.model_dump(exclude_unset=True)

    if "department_id" in update_data:
        await ensure_department(db, update_data["department_id"])

    for field, value in update_data.items():
        setattr(course, field, value)

    await db.commit()
    await db.refresh(course)

    return course


@app.delete(
    "/api/v1/courses/{course_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Courses"],
)
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    course = await db.get(Course, course_id)

    if course is None:
        not_found("Course", course_id)

    await db.delete(course)
    await db.commit()


@app.get(
    "/api/v1/courses/{course_id}/students/",
    response_model=list[StudentResponse],
    tags=["Courses"],
)
async def get_students_by_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    course = await db.get(Course, course_id)

    if course is None:
        not_found("Course", course_id)

    query = (
        select(Student)
        .join(Enrollment, Student.id == Enrollment.student_id)
        .where(Enrollment.course_id == course_id)
    )

    result = await db.execute(query)
    return result.scalars().all()


# ==================================================
# STUDENTS
# ==================================================


@app.post(
    "/api/v1/students/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
)
async def create_student(
    student: StudentCreate,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    await ensure_department(db, student.department_id)

    new_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=str(student.email),
        department_id=student.department_id,
        enrollment_year=student.enrollment_year,
    )

    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)

    response.headers["Location"] = f"/api/v1/students/{new_student.id}/"

    return new_student


@app.get(
    "/api/v1/students/",
    response_model=list[StudentResponse],
    tags=["Students"],
)
async def get_students(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Student))
    return result.scalars().all()


@app.get(
    "/api/v1/students/{student_id}/",
    response_model=StudentResponse,
    tags=["Students"],
)
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    student = await db.get(Student, student_id)

    if student is None:
        not_found("Student", student_id)

    return student


@app.put(
    "/api/v1/students/{student_id}/",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    tags=["Students"],
)
async def update_student(
    student_id: int,
    student_update: StudentUpdate,
    db: AsyncSession = Depends(get_db),
):
    student = await db.get(Student, student_id)

    if student is None:
        not_found("Student", student_id)

    await ensure_department(db, student_update.department_id)

    student.first_name = student_update.first_name
    student.last_name = student_update.last_name
    student.email = str(student_update.email)
    student.department_id = student_update.department_id
    student.enrollment_year = student_update.enrollment_year

    await db.commit()
    await db.refresh(student)

    return student


@app.delete(
    "/api/v1/students/{student_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Students"],
)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    student = await db.get(Student, student_id)

    if student is None:
        not_found("Student", student_id)

    await db.delete(student)
    await db.commit()


# ==================================================
# ENROLLMENTS
# ==================================================


@app.post(
    "/api/v1/enrollments/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"],
)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    response: Response,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    student = await db.get(Student, enrollment.student_id)

    if student is None:
        not_found("Student", enrollment.student_id)

    course = await db.get(Course, enrollment.course_id)

    if course is None:
        not_found("Course", enrollment.course_id)

    new_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        enrollment_date=enrollment.enrollment_date,
        grade=enrollment.grade,
    )

    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)

    response.headers["Location"] = (
        f"/api/v1/enrollments/{new_enrollment.id}/"
    )

    background_tasks.add_task(
        send_confirmation_email,
        student.email,
    )

    return new_enrollment


@app.get(
    "/api/v1/enrollments/",
    response_model=list[EnrollmentResponse],
    tags=["Enrollments"],
)
async def get_enrollments(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Enrollment))
    return result.scalars().all()


@app.get(
    "/api/v1/enrollments/{enrollment_id}/",
    response_model=EnrollmentResponse,
    tags=["Enrollments"],
)
async def get_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db),
):
    enrollment = await db.get(Enrollment, enrollment_id)

    if enrollment is None:
        not_found("Enrollment", enrollment_id)

    return enrollment


@app.put(
    "/api/v1/enrollments/{enrollment_id}/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_200_OK,
    tags=["Enrollments"],
)
async def update_enrollment(
    enrollment_id: int,
    enrollment_update: EnrollmentUpdate,
    db: AsyncSession = Depends(get_db),
):
    enrollment = await db.get(Enrollment, enrollment_id)

    if enrollment is None:
        not_found("Enrollment", enrollment_id)

    student = await db.get(Student, enrollment_update.student_id)
    if student is None:
        not_found("Student", enrollment_update.student_id)

    course = await db.get(Course, enrollment_update.course_id)
    if course is None:
        not_found("Course", enrollment_update.course_id)

    enrollment.student_id = enrollment_update.student_id
    enrollment.course_id = enrollment_update.course_id
    enrollment.enrollment_date = enrollment_update.enrollment_date
    enrollment.grade = enrollment_update.grade

    await db.commit()
    await db.refresh(enrollment)

    return enrollment


@app.delete(
    "/api/v1/enrollments/{enrollment_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Enrollments"],
)
async def delete_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db),
):
    enrollment = await db.get(Enrollment, enrollment_id)

    if enrollment is None:
        not_found("Enrollment", enrollment_id)

    await db.delete(enrollment)
    await db.commit()