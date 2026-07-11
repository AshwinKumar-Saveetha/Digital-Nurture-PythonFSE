from datetime import datetime, timedelta, timezone
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
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from jose import JWTError, jwt

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import create_tables, get_db
from models import Course, Department, Enrollment, Student, User
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
    TokenResponse,
    UserRegister,
    UserResponse,
)
from security import get_password_hash, verify_password

app = FastAPI(
    title="Course Management API",
    description=(
        "FastAPI Course Management API with RESTful naming, API versioning, "
        "pagination, filtering, standardised errors, Background Tasks, "
        "JWT authentication, CORS, and OpenAPI documentation."
    ),
    version="1.0",
    contact={
        "name": "Ashwin Kumar A",
        "email": "ashwin@example.com",
    },
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


SECRET_KEY = "hands-on-9-course-management-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/",
)


def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    # JWT payloads are encoded and signed, but they are not encrypted.
    # Never place passwords, card details, or other sensitive data in a JWT.
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# OAuth2 Authorization Code flow:
# The user is redirected to an authorisation server and signs in there.
# The client receives a short-lived authorisation code and exchanges it for
# an access token. This keeps the user's credentials away from the client
# application and is commonly used with third-party identity providers.
#
# This Hands-On uses a simpler first-party JWT login. The API directly
# receives the user's email and password, verifies them, and immediately
# issues a JWT. It does not use redirects, an authorisation code, or a
# separate authorisation server.

# API versioning note:
# URL versioning, such as /api/v1/courses/, is simple, explicit, and easy
# to test in browsers and API clients.
# Header-based versioning keeps URLs cleaner but requires clients to send
# a version in a header such as:
# Accept: application/vnd.api+json;version=1


@app.on_event("startup")
async def startup_event() -> None:
    await create_tables()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "code": "INVALID_TOKEN",
            "message": "Could not validate authentication credentials",
            "field": None,
        },
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        email = payload.get("sub")

        if not isinstance(email, str) or not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise credentials_exception

    return user


@app.post(
    "/api/v1/auth/register/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"],
    summary="Register a new user",
    response_description="The registered user without the password",
)
async def register_user(
    user_data: UserRegister,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> User:
    normalised_email = str(user_data.email).lower()

    existing_result = await db.execute(
        select(User).where(User.email == normalised_email)
    )
    existing_user = existing_result.scalar_one_or_none()

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "EMAIL_ALREADY_REGISTERED",
                "message": "A user with this email is already registered",
                "field": "email",
            },
        )

    # The plain-text password is used only to create the bcrypt hash.
    # It is never stored or logged.
    new_user = User(
        email=normalised_email,
        hashed_password=get_password_hash(user_data.password),
        is_active=True,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    response.headers["Location"] = f"/api/v1/auth/users/{new_user.id}/"

    return new_user


@app.post(
    "/api/v1/auth/login/",
    response_model=TokenResponse,
    tags=["Authentication"],
    summary="Login and receive a JWT access token",
)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    email = form_data.username.lower()

    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if user is None or not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INVALID_CREDENTIALS",
                "message": "Incorrect email or password",
                "field": None,
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INACTIVE_USER",
                "message": "The user account is inactive",
                "field": None,
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        subject=user.email,
        expires_delta=timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


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
    current_user: User = Depends(get_current_user),
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
    current_user: User = Depends(get_current_user),
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