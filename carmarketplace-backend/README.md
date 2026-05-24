# FastAPI Beginner Boilerplate 🚀

A **beginner-friendly FastAPI boilerplate** with clean architecture, JWT authentication, and MySQL database support.

This project is designed for:
- Beginners learning FastAPI
- Clean code & folder structure
- Real-world backend practices
- Easy scaling for future features

---

## ✨ Features

- FastAPI
- MySQL + SQLAlchemy ORM
- JWT Authentication (Login/Register)
- Password Hashing (bcrypt)
- Modular Folder Structure
- Dependency Injection
- Beginner Friendly Code

---

## 📁 Project Structure

app/
├── core/ # security, config
├── db/ # database connection
├── models/ # SQLAlchemy models
├── schemas/ # Pydantic schemas
├── cruds/ # Database logic
├── routers/ # API routes
└── main.py # Application entry

---

## 🛠️ Requirements

- Python 3.10+
- MySQL
- pip

---

## 📦 Packages Used

- fastapi
- uvicorn
- sqlalchemy
- pymysql
- python-jose
- passlib[bcrypt]
- python-dotenv

## 🛠️ Tech Stack
- **Backend:** FastAPI
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Auth:** JWT (python-jose)
- **Security:** Passlib (bcrypt)

2️⃣ Create Virtual Environment

python -m venv .venv

3️⃣ Activate Virtual Environment

.\.venv\Scripts\Activate.ps1

4️⃣ Install Dependencies

pip install -r requirements.txt

5️⃣ Run the Application

uvicorn app.main:app --reload
