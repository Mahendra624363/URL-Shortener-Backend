# URL-Shortener-Backend

# 🔗 URL Shortener Backend (Django + JWT)

A backend system built using Django REST Framework that provides:

- JWT Authentication (Register/Login/Logout)
- Email Verification
- URL Shortener Service
- Per-user limit (max 10 URLs)
- Public URL redirection
- Unit + integration tests (~99% coverage)

---

# 🚀 Features

## 🔐 Authentication
- User registration
- Email verification using UUID token
- JWT login (access + refresh tokens)
- Logout with token blacklist
- Protected user profile API

## 🔗 URL Shortener
- Convert long URLs into short codes
- Redirect short code → original URL
- Public access for redirection (no login required)

## 📊 Rate Limiting
- Each user can create **maximum 10 shortened URLs**

## 🧪 Testing
- Unit tests
- Integration tests
- ~99% test coverage

---

# 🛠️ Tech Stack

- Django
- Django REST Framework
- SimpleJWT
- SQLite / PostgreSQL
- Django Test Framework

---

# 📁 Project Structure

```bash
url-shortener/
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   ├── tests.py
│
├── app/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   ├── tests.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│
├── manage.py
├── requirements.txt
├── .env
└── README.md
```

---

# 🌐 API ENDPOINTS

## 🔐 AUTHENTICATION APIs

### Register User
```http
POST /accounts/register/
```

```json
{
  "email": "user@gmail.com",
  "password": "123456"
}
```

---

### Email Verification
```http
GET /accounts/verify/<uuid:token>/
```

---

### Login (JWT)
```http
POST /accounts/login/
```

```json
{
  "email": "user@gmail.com",
  "password": "123456"
}
```

```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```

---

### Refresh Token
```http
POST /accounts/refresh/
```

```json
{
  "refresh": "your_refresh_token"
}
```

---

### Logout
```http
POST /accounts/logout/
```

---

### Profile (Protected)
```http
GET /accounts/profile/
Authorization: Bearer <access_token>
```

---

## 🔗 URL SHORTENER APIs

### Create Short URL
```http
POST /shorten/
Authorization: Bearer <access_token>
```

```json
{
  "original_url": "https://example.com"
}
```

```json
{
  "short_url": "http://127.0.0.1:8000/aZ91k"
}
```

---

### Redirect Short URL
```http
GET /<short_code>/
```

Example:
```http
GET /aZ91k/
```

➡ Redirects to original URL (HTTP 302)

---

# ⚙️ SETUP INSTRUCTIONS

## 1. Clone Repository
```bash
git clone https://github.com/your-username/url-shortener.git
cd url-shortener
```

## 2. Create Virtual Environment
```bash
python -m venv venv
```

Activate:

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 5. Run Server
```bash
python manage.py runserver
```

---

# 🧪 TESTING

```bash
python manage.py test
coverage run manage.py test
coverage report -m
```

---

# 🔐 BUSINESS LOGIC

- Each user can create max **10 URLs**
- JWT authentication required for creation APIs
- Redirect API is public

---

🔥 :contentReference[oaicite:2]{index=2}

Just tell 👍
