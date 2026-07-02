# Module 3: Database Integration

Digital Nurture 5.0 - Python Full Stack Engineer Track
Hands-On Exercise Book solutions - Student Course Registration System

This project implements all 7 hands-on exercises from the Module 3
exercise book: schema design, SQL DML/joins/aggregation, advanced
SQL (subqueries/views/procedures/transactions), query optimisation,
MongoDB, SQLAlchemy ORM integration, and Alembic migrations.

## Tech stack

- **MySQL 8.x** for all relational SQL exercises (Hands-On 1-4)
- **MongoDB** (mongosh / Compass) for Hands-On 5
- **SQLAlchemy** for the ORM layer (Hands-On 6)
- **Alembic** for schema migrations (Hands-On 7)
- **Python 3.10+**

## Project layout

```
Module3_DatabaseIntegration/
├── hands_on_1.sql        # Schema design, DDL, normalisation
├── hands_on_2.sql        # DML, joins, aggregations
├── hands_on_3.sql        # Subqueries, views, procedures, transactions
├── hands_on_4.sql        # Indexes, EXPLAIN, N+1 problem
├── hands_on_5.sql        # MongoDB CRUD & aggregation (mongosh syntax)
├── hands_on_6.sql        # Pointer to orm/ (ORM is Python, not SQL)
├── hands_on_7.sql        # Pointer to migrations/ (Alembic CLI, not SQL)
├── orm/
│   ├── models.py          # SQLAlchemy models
│   ├── crud.py             # CRUD + N+1 fix demo
│   ├── n_plus_one_demo.py  # Standalone query-count/timing demo
│   ├── requirements.txt
│   └── README.md
├── migrations/
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   ├── README
│   └── versions/
│       ├── initial_schema.py
│       ├── add_is_active.py
│       └── add_course_schedule.py
├── README.md              (this file)
└── requirements.txt
```

## Setup

### 1. MySQL (Hands-On 1-4)

```bash
mysql -u root -p < hands_on_1.sql
mysql -u root -p < hands_on_2.sql
mysql -u root -p < hands_on_3.sql
mysql -u root -p < hands_on_4.sql
```

Run them in this exact order - each file builds on the schema and
data created by the previous one.

### 2. MongoDB (Hands-On 5)

```bash
mongosh < hands_on_5.sql
```

(The file is MongoDB Shell syntax; it keeps the `.sql` extension
only to match the required project layout - see the note at the
top of the file.)

### 3. Python environment (Hands-On 6 & 7)

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. ORM (Hands-On 6)

```bash
mysql -u root -p -e "CREATE DATABASE college_db_orm;"
export COLLEGE_DB_ORM_URL="mysql+mysqlconnector://root:YOUR_PASSWORD@localhost:3306/college_db_orm"

cd orm
python models.py             # creates tables
python crud.py                # CRUD demo + N+1 fix (echo=True logs every query)
python n_plus_one_demo.py     # Hands-On 4 Task 3: query-count/timing comparison
cd ..
```

### 5. Migrations (Hands-On 7)

```bash
cd migrations
alembic upgrade head          # apply all 3 revisions
alembic current                # show current head
alembic history --verbose      # show full migration chain
alembic downgrade -1           # step back one revision
alembic downgrade base         # undo all migrations
alembic upgrade head           # re-apply everything
cd ..
```

## Assumptions / design notes

- **MySQL, not PostgreSQL**: the exercise book allows either engine
  for Hands-On 1-4; this project standardises on MySQL 8.x per the
  stated requirements, using `AUTO_INCREMENT`, `CHANGE` for column
  renames, and `EXPLAIN FORMAT=JSON` throughout.
- **Partial indexes (Hands-On 4, Step 55)**: MySQL 8.x has no
  direct equivalent of PostgreSQL's `WHERE`-filtered partial index.
  `hands_on_4.sql` documents this limitation and uses a regular
  composite index as the closest practical substitute, with the
  true PostgreSQL syntax included as a comment for reference.
- **Hands-On 6 & 7 as `.sql` files**: both exercises are
  Python/Alembic-driven, not raw SQL. To satisfy the requested
  top-level layout, `hands_on_6.sql` and `hands_on_7.sql` are kept
  as documentation/pointer files that explain what each step maps
  to inside `orm/` and `migrations/`, where the actual runnable
  code lives.
- **N+1 demo placement (Hands-On 4, Task 3)**: since the required
  layout has no dedicated `scripts/` folder, the Python N+1 timing
  demo lives at `orm/n_plus_one_demo.py` and is referenced from
  `hands_on_4.sql`.
- **`college_db` vs `college_db_orm`**: the raw-SQL exercises
  (Hands-On 1-4) use `college_db`; the ORM/migrations exercises
  (Hands-On 6-7) use a separate `college_db_orm` database, exactly
  as specified in the exercise book (Step 79).
