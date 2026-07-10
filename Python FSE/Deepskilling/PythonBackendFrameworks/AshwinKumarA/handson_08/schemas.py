from typing import Optional
from pydantic import BaseModel, EmailStr


class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int


class CourseUpdate(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int


class CoursePatch(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None


class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    department_id: int

    model_config = {"from_attributes": True}


class CourseListEnvelope(BaseModel):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: list[CourseResponse]


class DepartmentResponse(BaseModel):
    id: int
    name: str
    head_of_dept: str
    budget: float
    courses: list[CourseResponse] = []

    model_config = {"from_attributes": True}


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    department_id: int
    enrollment_year: int


class StudentUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    department_id: int
    enrollment_year: int


class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department_id: int
    enrollment_year: int

    model_config = {"from_attributes": True}


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: str
    grade: Optional[str] = None


class EnrollmentUpdate(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: str
    grade: Optional[str] = None


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrollment_date: str
    grade: Optional[str] = None

    model_config = {"from_attributes": True}