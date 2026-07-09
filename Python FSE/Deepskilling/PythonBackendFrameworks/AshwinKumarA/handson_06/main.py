from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import create_tables, get_db
from models import Course, Department
from schemas import CourseCreate, CourseResponse, CourseUpdate


app = FastAPI(title="Course Management API", version="1.0")


@app.on_event("startup")
async def startup_event() -> None:
    await create_tables()


@app.get("/")
async def root():
    return {"message": "API running"}


@app.post(
    "/api/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_course(
    course: CourseCreate,
    db: AsyncSession = Depends(get_db),
):
    department = await db.get(Department, course.department_id)

    if department is None:
        department = Department(
            id=course.department_id,
            name=f"Department {course.department_id}",
        )
        db.add(department)
        await db.flush()

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


@app.get("/api/courses/", response_model=list[CourseResponse])
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
    courses = result.scalars().all()

    return courses


@app.get("/api/courses/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    course = await db.get(Course, course_id)

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    return course


@app.put("/api/courses/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course_update: CourseUpdate,
    db: AsyncSession = Depends(get_db),
):
    course = await db.get(Course, course_id)

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    update_data = course_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(course, field, value)

    await db.commit()
    await db.refresh(course)

    return course


@app.delete("/api/courses/{course_id}")
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    course = await db.get(Course, course_id)

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    await db.delete(course)
    await db.commit()

    return {"message": "Course deleted successfully"}