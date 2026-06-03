# Car Marketplace Backend

A **FastAPI backend** for a car marketplace with **AI-powered search** — search cars using natural language text or voice audio, which gets transcribed and converted into SQL queries via an LLM.

---

## Features

- JWT Authentication (Register / Login)
- Car CRUD (Create, Read, Update, Delete)
- Filtered car listing (brand, model, city, price range, mileage, etc.)
- **AI Text Search** — describe a car in plain English or Italian, get matching results
- **Voice Search** — upload an audio file, Whisper transcribes it, LLM converts it to SQL
- CORS enabled (open to all origins by default)
- Auto table creation on startup

---

## How It Works

```
Voice/Text Query
      │
      ▼
[Faster Whisper]  ←── (voice only, transcribes audio to text)
      │
      ▼
[Groq LLM - Llama 3.3 70B]  ←── converts natural language to PostgreSQL SELECT
      │
      ▼
[PostgreSQL / MySQL Database]  ←── executes query, returns car results
```

The LLM only generates `SELECT` queries — write operations (`INSERT`, `UPDATE`, `DELETE`, `DROP`, etc.) are blocked before execution.

---

## Project Structure

```
app/
├── core/
│   └── security.py       # JWT creation/validation, bcrypt password hashing
├── db/
│   └── database.py       # SQLAlchemy engine and session setup
├── models/
│   ├── user.py           # User table model
│   └── carInfo.py        # Cars table model
├── schemas/
│   ├── user.py           # User Pydantic schemas
│   └── carInfo.py        # Car Pydantic schemas (create, update, response, AI/voice search)
├── crud/
│   ├── user.py           # User DB operations
│   └── car.py            # Car DB operations + raw SQL executor
├── routers/
│   ├── auth.py           # /register, /login
│   ├── users.py          # /users
│   └── carInfo.py        # /cars (CRUD + AI search + voice search)
├── services/
│   ├── llm_service.py    # Groq API client — natural language to SQL
│   └── voice_service.py  # Faster Whisper — audio transcription
└── main.py               # App entry point, middleware, router registration
```

---

## API Endpoints

### Auth
| Method | Endpoint    | Description              | Auth |
|--------|-------------|--------------------------|------|
| POST   | `/register` | Register a new user      | No   |
| POST   | `/login`    | Login, returns JWT token | No   |

### Users
| Method | Endpoint  | Description       | Auth     |
|--------|-----------|-------------------|----------|
| GET    | `/users/` | List all users    | Required |

### Cars
| Method | Endpoint               | Description                              | Auth     |
|--------|------------------------|------------------------------------------|----------|
| POST   | `/cars/`               | Add a new car listing                    | Required |
| GET    | `/cars/`               | List cars with optional filters          | No       |
| GET    | `/cars/ai-search`      | Natural language search (text query)     | No       |
| POST   | `/cars/voice-search`   | Upload audio, search by voice            | No       |
| GET    | `/cars/{car_id}`       | Get a single car by ID                   | No       |
| PUT    | `/cars/{car_id}`       | Update a car listing                     | Required |
| DELETE | `/cars/{car_id}`       | Delete a car listing                     | Required |

#### `GET /cars/` — Filter Parameters
`name`, `brand`, `model`, `city`, `color`, `fuel_type`, `transmission`, `year`, `min_price`, `max_price`, `min_mileage`, `max_mileage`

#### `GET /cars/ai-search` — Query Parameter
`query` — plain English or Italian description, e.g. `red Toyota automatic under 20000`

#### `POST /cars/voice-search` — Form Data
`audio` — audio file (any common format), spoken car description in English or Italian

---

## Car Model Fields

| Field          | Type    | Notes                                      |
|----------------|---------|--------------------------------------------|
| `name`         | string  | Listing title                              |
| `brand`        | string  | e.g. Toyota, BMW                           |
| `model`        | string  | e.g. Corolla, X5                           |
| `city`         | string  |                                            |
| `color`        | string  |                                            |
| `price`        | float   |                                            |
| `year`         | integer |                                            |
| `mileage`      | integer | In km                                      |
| `fuel_type`    | string  | Petrol / Diesel / Electric / Hybrid        |
| `transmission` | string  | Automatic / Manual                         |
| `condition`    | string  | New / Used                                 |
| `images`       | string  | Optional image URL                         |
| `description`  | string  | Optional free text                         |

---

## Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Framework    | FastAPI 0.128                       |
| ORM          | SQLAlchemy 2.0                      |
| Database     | PostgreSQL (psycopg2) / MySQL (PyMySQL) |
| Auth         | JWT via python-jose                 |
| Passwords    | passlib bcrypt_sha256               |
| LLM          | Groq API — Llama 3.3 70B Versatile  |
| Transcription| Faster Whisper (base, CPU, int8)    |
| Config       | python-dotenv                       |

---

## Setup

### 1. Clone and create virtual environment

```bash
git clone <repo-url>
cd carmarketplace-backend
python -m venv .venv
```

### 2. Activate virtual environment

```powershell
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/carmarketplace
SECRET_KEY=your-secret-key
ALGORITHM=HS256
GROQ_API_KEY=your-groq-api-key
```

Get a free Groq API key at [console.groq.com](https://console.groq.com).

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.  
Interactive docs: `http://127.0.0.1:8000/docs`

---

## AI Search — Supported Languages

The LLM accepts queries in **English** and **Italian** only. Queries in other languages, irrelevant questions, or prompt injection attempts return a structured error response.

```json
{"error": "Language not supported. Please write in English or Italian."}
```

---

## Requirements

- Python 3.10+
- PostgreSQL or MySQL
- Groq API key (free tier available)
