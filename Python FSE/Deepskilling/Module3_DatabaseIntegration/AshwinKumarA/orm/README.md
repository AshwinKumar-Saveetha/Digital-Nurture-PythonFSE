# orm/ - SQLAlchemy ORM Integration (Hands-On 6)

Python/SQLAlchemy implementation of Hands-On 6, plus the standalone
N+1 timing demo referenced from Hands-On 4, Task 3.

## Files

| File                  | Purpose                                                              |
|------------------------|-----------------------------------------------------------------------|
| `models.py`            | SQLAlchemy model classes + engine (Task 1, Steps 75-79)              |
| `crud.py`               | INSERT/READ/UPDATE/DELETE + N+1 fix with `joinedload` (Task 2 & 3)   |
| `n_plus_one_demo.py`    | Standalone query-count/timing demo referenced from Hands-On 4        |
| `requirements.txt`      | Python dependencies for this folder                                  |

## Setup

1. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create the target database in MySQL (empty is fine - SQLAlchemy
   creates the tables for you):

   ```sql
   CREATE DATABASE college_db_orm;
   ```

4. Point the code at your MySQL instance. `models.py` reads the
   connection string from the `COLLEGE_DB_ORM_URL` environment
   variable, falling back to a local default if it's not set:

   ```bash
   export COLLEGE_DB_ORM_URL="mysql+mysqlconnector://root:YOUR_PASSWORD@localhost:3306/college_db_orm"
   ```

## Run

```bash
python models.py            # Step 79: creates all tables (departments,
                             # students, courses, enrollments, professors,
                             # course_schedules) in college_db_orm

python crud.py               # Steps 80-91: CRUD demo + N+1 fix, with
                              # full SQL logging (echo=True) so you can
                              # count queries in the console output

python n_plus_one_demo.py    # Hands-On 4, Task 3: prints exact query
                              # counts and timings for the naive vs
                              # JOIN-based approach
```

> Note: this project standardises on MySQL 8.x per the assignment
> requirements. If you prefer to run against PostgreSQL instead,
> swap the connection string's driver to `postgresql+psycopg2://...`
> and install `psycopg2-binary` - the SQLAlchemy model code itself
> does not change.
