# Full Authentication and User Management System

A production-style REST API built with **FastAPI**, **MongoDB**, **Pydantic**, and **Pytest**. This system features JWT authentication, role-based access control (RBAC), password hashing, soft deletes, user profile management, admin controls, filtering, pagination, and real-time user statistics.

---

## 🛠 Tech Stack & Tools

* **Framework:** FastAPI (Python)
* **Database:** MongoDB
* **Authentication:** JWT (JSON Web Tokens)
* **Password Hashing:** Passlib (Bcrypt / Argon2)
* **Data Validation:** Pydantic
* **Testing:** Pytest (Async/AnyIO)

---

## 📂 Project Structure

```text
user_management_api/
├── app/
│   ├── core/           # Security, JWT, and dependency utilities
│   ├── database.py     # MongoDB database connections
│   ├── main.py         # FastAPI application entry point
│   ├── models/         # Pydantic schemas & UserRole definitions
│   ├── routers/        # API Endpoints (auth, users, stats)
│   └── services/      # Business logic & Database queries
├── tests/              # Automated unit/integration test suites
├── requirements.txt    # Project dependencies
└── README.md           # Documentation


🔐 Key Features & Business RulesSelf-Registration: Public registration (POST /register) automatically assigns the client role. Users cannot choose their role.Role-Based Authorization:Client: Accesses and updates their own profile (/users/me).Admin: Manages all users, changes roles, creates admin accounts (POST /users), and performs soft deletes.Soft Delete: Deleted users are marked with is_deleted: true and a timestamp (deleted_at). They cannot log in and are excluded from standard user listings and public statistics.Pagination & Filtering: Admin listing (GET /users) supports filtering by city, age, type, first_name, last_name, and email, alongside page-based pagination.Public Statistics: Real-time stats on total active users, average age, and top 3 cities without requiring authentication.

🚀 Getting Started1. Installation & Environment SetupActivate your virtual environment and install dependencies:Bash# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
2. Running the API ServerStart the local server using Uvicorn:Bashuvicorn app.main:app --reload
The server will start at http://127.0.0.1:8000.3. API Documentation (Swagger UI)FastAPI automatically generates interactive documentation:Swagger UI: http://127.0.0.1:8000/docsReDoc: http://127.0.0.1:8000/redoc🧪 Running Automated TestsRun the full Pytest test suite to verify endpoints, authorization checks, soft-delete mechanics, and statistics:Bashpython -m pytest tests/ -v

📌 API Routes SummaryMethodEndpointAccessPurposePOST/registerPublicRegister as a new clientPOST/loginPublicAuthenticate and obtain JWT tokenGET/users/meAuthenticatedView current logged-in user profilePUT/users/meAuthenticatedUpdate current user profileGET/usersAdminGet paginated & filtered active usersPOST/usersAdminCreate a new user (client or admin)GET/users/{id}AdminGet user details by IDPUT/users/{id}AdminUpdate user details or role by IDDELETE/users/{id}AdminSoft-delete a userGET/stats/countPublicActive user countGET/stats/average-agePublicAverage age of active usersGET/stats/top-citiesPublicTop 3 cities by active user count


## 📌 API Routes Summary

| Method | Endpoint | Access | Purpose |
| :--- | :--- | :--- | :--- |
| `POST` | `/register` | Public | Register as a new client |
| `POST` | `/login` | Public | Authenticate and obtain JWT token |
| `GET` | `/users/me` | Authenticated | View current logged-in user profile |
| `PUT` | `/users/me` | Authenticated | Update current user profile |
| `GET` | `/users` | Admin | Get paginated & filtered active users |
| `POST` | `/users` | Admin | Create a new user (client or admin) |
| `GET` | `/users/{id}` | Admin | Get user details by ID |
| `PUT` | `/users/{id}` | Admin | Update user details or role by ID |
| `DELETE` | `/users/{id}` | Admin | Soft-delete a user |
| `GET` | `/stats/count` | Public | Active user count |
| `GET` | `/stats/average-age` | Public | Average age of active users |
| `GET` | `/stats/top-cities` | Public | Top 3 cities by active user count |