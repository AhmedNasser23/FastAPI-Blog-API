# FastAPI Blog API

A production-ready RESTful API built with **FastAPI**, featuring user authentication, post management, voting, and containerized deployment.  
This project was developed as part of learning API development and backend engineering.

---

## 🚀 Features
- **User Authentication**: Secure login/registration with JWT tokens.
- **Post Management**: Full CRUD functionality for blog posts.
- **Voting System**: Upvote/downvote feature with relational data integrity.
- **Database Integration**: PostgreSQL with SQLAlchemy ORM and Alembic migrations.
- **Testing**: Automated test suite using Pytest for reliability.
- **Deployment Ready**: Containerized with Docker for consistent dev & production.

---

## 🛠️ Tech Stack
- **Language**: Python 3
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Containerization**: Docker
- **Testing**: Pytest

---

## 📂 Project Structure
```
.
├── app
│   ├── main.py          # Application entry point
│   ├── models.py        # Database models
│   ├── schemas.py       # Pydantic schemas
│   ├── database.py      # DB connection
│   ├── config.py        # 
│   ├── oauth2.py        # 
│   └── utils.py         # Utility functions
│   ├── routers/         # API routes (users, posts, auth, votes)
├── tests/               # Pytest test cases
├── requirements.txt     # Project dependencies
├── Dockerfile           # Docker configuration
└── README.md
```

---

## ⚡ Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/FastAPI-Blog-API.git
cd FastAPI-Blog-API
```

### 2. Create a virtual environment & install dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows
pip install -r requirements.txt
```

### 3. Set environment variables
Create a `.env` file in the root directory and define:
```
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=yourpassword
DATABASE_NAME=fastapi
DATABASE_USERNAME=yourusername
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Run database migrations
```bash
alembic upgrade head
```

### 5. Start the API
```bash
uvicorn app.main:app --reload
```

API will be available at:  
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🐳 Run with Docker
Build and run the container:
```bash
docker-compose up --build
```

---

## ✅ Testing
Run all tests with:
```bash
pytest
```

---

## 📌 Endpoints Overview
- `POST /users/` → Register a new user  
- `POST /login` → User login & JWT token generation  
- `GET /posts/` → Get all posts  
- `POST /posts/` → Create a new post  
- `PUT /posts/{id}` → Update a post  
- `DELETE /posts/{id}` → Delete a post  
- `POST /vote/` → Vote on a post  

Interactive API docs available at:  
- Swagger UI → `/docs`  
- ReDoc → `/redoc`  

---

## 📜 License
This project is licensed under the MIT License.
