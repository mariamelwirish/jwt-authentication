# FastAPI JWT Authentication

A JWT authentication system built with FastAPI and PostgreSQL. Covers user signup, login, password hashing, token generation, and protected routes.

Built as a learning project before working on a larger full-stack application.

---

## What it does

- User signup with hashed passwords (bcrypt)
- User login with JWT token generation
- Protected routes that require a valid token
- Clean layered architecture — routers, services, repositories, schemas

---

## Tech stack

- **FastAPI** — web framework
- **PostgreSQL** — database (runs via Docker)
- **SQLAlchemy** — ORM
- **Pydantic** — data validation
- **bcrypt** — password hashing
- **PyJWT** — JWT token generation and verification
- **python-decouple** — environment variable management

---

## Project structure

```
fastapi_jwt/
├── app/
│   ├── core/
│   │   ├── database.py          # SQLAlchemy engine, session, Base
│   │   └── security/
│   │       ├── authHandler.py   # JWT generation and decoding
│   │       └── hashHelper.py    # Password hashing and verification
│   ├── db/
│   │   ├── models/
│   │   │   └── user.py          # User table definition
│   │   ├── schema/
│   │   │   └── user.py          # Pydantic schemas
│   │   └── repository/
│   │       ├── base.py          # Base repository with session
│   │       └── userRepo.py      # User database queries
│   ├── routers/
│   │   └── auth.py              # Login and signup routes
│   ├── service/
│   │   └── userService.py       # Business logic
│   └── util/
│       ├── init_db.py           # Table creation on startup
│       └── protectRoute.py      # JWT validation dependency
├── .env                         # Environment variables (not committed)
├── .gitignore
├── main.py
└── requirements.txt
```

---

## Getting started

### Prerequisites

- Python 3.12+
- Docker

### 1. Clone the repo

```bash
git clone https://github.com/mariamelwirish/jwt-authentication.git
cd jwt-authentication
```

### 2. Start the PostgreSQL container

```bash
docker run -d --name postgres-db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -p 5432:5432 postgres
```

### 3. Create a virtual environment

Mac/Linux:
```bash
python3 -m venv venv
```

Windows:
```bash
python -m venv venv
```

### 4. Activate the virtual environment

Mac/Linux:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Set up environment variables

Create a `.env` file in the root directory:

```
DB_USER=user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_SERVER=postgres
JWT_SECRET=your_secret_key_here
JWT_ALGORITHM=HS256
```

### 7. Run the app

```bash
fastapi dev main.py
```

The app will be running at `http://127.0.0.1:8000`.
Interactive docs at `http://127.0.0.1:8000/docs`.

---

## API endpoints

### POST /auth/signup

Create a new user account.

Request body:
```json
{
    "first_name": "Mariam",
    "last_name": "Elwirish",
    "email": "mariamelwirish@jwt.fastapi",
    "password": "password123"
}
```

Response:
```json
{
    "id": 1,
    "first_name": "Mariam",
    "last_name": "Elwirish",
    "email": "mariamelwirish@jwt.fastapi"
}
```

---

### POST /auth/login

Login with existing credentials and receive a JWT token.

Request body:
```json
{
    "email": "mariamelwirish@jwt.fastapi",
    "password": "password123"
}
```

Response:
```json
{
    "token": "eyJhbGciOiJIUzI1NiJ9..."
}
```

---

### GET /protected

A protected route that requires a valid JWT token.

Headers:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...
```

Response:
```json
{
    "message": "Hello, Mariam Elwirish! This is a protected route."
}
```

---

## How authentication works

1. User signs up — password is hashed with bcrypt before being stored
2. User logs in — bcrypt verifies the password against the stored hash
3. On successful login — a JWT token is generated with the user's ID and an expiry time embedded in the payload
4. For protected routes — the token is sent in the `Authorization` header, the server verifies the signature, checks expiry, extracts the user ID, and queries the database for that user