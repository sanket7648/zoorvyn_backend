# Finance Dashboard Backend

This repository contains the backend API for a finance dashboard system. It is designed to manage users, handle role-based access control (RBAC), process financial records, and serve aggregated dashboard analytics. 

The project is built using Python, FastAPI, and PostgreSQL, with a focus on maintainability, data validation, and clean separation of concerns.

## Tech Stack
* **Framework:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy 2.0
* **Migrations:** Alembic
* **Validation:** Pydantic
* **Authentication:** JWT (JSON Web Tokens) with Passlib (bcrypt)

## Project Structure
The application follows a modular, feature-based directory structure (Controller-Service-Repository pattern adapted for FastAPI) to ensure separation of concerns:

* `app/api/`: Route definitions and dependency injection (Auth, RBAC).
* `app/core/`: Application configurations, security utilities, and environment settings.
* `app/db/`: Database session management and connection setup.
* `app/models/`: SQLAlchemy ORM classes (Database schema).
* `app/schemas/`: Pydantic models for request/response validation.
* `alembic/`: Database migration scripts.

## Local Setup & Installation

### 1. Prerequisites
* Python 3.10+
* PostgreSQL installed and running locally

### 2. Environment Setup
Clone the repository and set up a virtual environment:

```bash
1. python -m venv venv
2. source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

3. Environment Variables
Create a .env file in the root directory and add your database credentials and secret key:

DATABASE_URL=postgresql://<username>:<password>@localhost:5432/finance_db
SECRET_KEY=your_super_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30

4. Database Initialization
Ensure you have created an empty PostgreSQL database named finance_db. Then, run the Alembic migrations to generate the tables:

alembic upgrade head

5. Running the Application
Start the FastAPI development server:
uvicorn app.main:app --reload

The API will be available at http://localhost:8000.
Interactive Swagger API documentation is automatically generated at http://localhost:8000/docs.

Access Control & Roles
The system enforces strict role-based access using FastAPI dependency injection.

Admin: Full access. Can create, read, update, and delete financial records. Can also view all users and deactivate accounts.

Analyst: Read-only access to raw financial records and full access to dashboard summaries.

Viewer: Restricted from accessing raw financial records. Can only access the dashboard summary aggregations.

API Overview
Authentication (/api/auth)
POST /register: Register a new user (requires email, password, and role).

POST /login: Authenticate and receive a JWT Bearer token.

Financial Records (/api/records)
GET /: List records with optional pagination and filtering (transaction_type, category, start_date, end_date).

POST /: Create a new record (Admin only).

GET /{id}: Retrieve a specific record.

PUT /{id}: Update a record (Admin only).

DELETE /{id}: Delete a record (Admin only).

Dashboard Analytics (/api/dashboard)
GET /summary: Returns aggregated data calculated directly in PostgreSQL (total income, total expense, net balance, category totals, and recent transactions). Available to all authenticated roles.

User Management (/api/users)
GET /: List all users (Admin only).

PUT /{id}/status: Activate or deactivate a user account (Admin only).

Design Decisions & Assumptions
Data Types for Currency: The amount field in the database is modeled as a Numeric(10, 2) rather than a standard float to prevent floating-point arithmetic errors, which is critical for financial data.

Database Aggregations: Dashboard analytics (sums, groupings) are executed at the database level using SQLAlchemy's func methods. This is significantly more efficient than fetching all records into Python memory and calculating totals iteratively.

Input Validation: Pydantic schemas enforce strict data validation before requests hit the database (e.g., ensuring financial amounts are greater than 0, limiting categories to specific strings).

Deactivation vs Deletion: Instead of hard-deleting users, an is_active boolean flag is used. If an admin deactivates an account, the dependency injector will catch it and block that user from authenticating or accessing endpoints, preserving their historical transaction data.