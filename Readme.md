# HR Management System - Backend

Backend REST API for a Human Resources Management System developed with Django REST Framework.

This project provides secure authentication using JWT and serves as the backend for a Flutter Desktop and Mobile application.

---

# Technologies

- Python 3.12
- Django 6.0.6
- Django REST Framework
- Simple JWT
- drf-spectacular (Swagger)
- SQLite (Development)
- SMTP Gmail
- Python Decouple

---

# Features Implemented

## Authentication Module

### User Login

Authenticate users using:

- Email
- Password

Returns:

- JWT Access Token
- JWT Refresh Token
- User information

Endpoint

POST

```
/api/auth/login/
```

---

### Current User

Return information about the authenticated user.

Endpoint

GET

```
/api/auth/me/
```

---

### Logout

Invalidate the Refresh Token using JWT Blacklist.

Endpoint

POST

```
/api/auth/logout/
```

---

### Refresh Token

Generate a new Access Token.

Endpoint

POST

```
/api/auth/refresh/
```

---

### Forgot Password

Send a password reset email.

Endpoint

POST

```
/api/auth/forgot-password/
```

---

### Reset Password

Reset the user's password using a secure token.

Endpoint

POST

```
/api/auth/reset-password/
```

---

# Project Structure

```
backend/

│

├── apps/

│ ├── authentication/

│ ├── users/

│ ├── employees/

│

├── config/

├── media/

├── static/

├── manage.py

└── requirements.txt
```

---

# Authentication Flow

```
Login

↓

Access Token
Refresh Token

↓

Authenticated Requests

↓

/api/auth/me

↓

Logout
```

---

# Password Reset Flow

```
Forgot Password

↓

Email

↓

Reset Link

↓

Reset Password

↓

Login
```

---

# API Documentation

Swagger

```
http://127.0.0.1:8000/api/docs/swagger/
```

Redoc

```
http://127.0.0.1:8000/api/docs/redoc/
```

---

# Installation

Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/hr-management-backend.git
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run migrations

```bash
python manage.py migrate
```

Create superuser

```bash
python manage.py createsuperuser
```

Run server

```bash
python manage.py runserver
```

---

# Environment Variables

Create a `.env` file.

Example

```env
SECRET_KEY=

DEBUG=True

EMAIL_BACKEND=

EMAIL_HOST=

EMAIL_PORT=

EMAIL_HOST_USER=

EMAIL_HOST_PASSWORD=

EMAIL_USE_TLS=True

DEFAULT_FROM_EMAIL=

FRONTEND_URL=
```

---

# Implemented Modules

- Authentication
- User Management
- Employee Profile

---

# Modules Under Development

- Departments
- Attendance
- Leave Management
- Payroll
- Notifications
- Reports
- Dashboard

---

# Author

Backend Developer

Oumeima Belala
