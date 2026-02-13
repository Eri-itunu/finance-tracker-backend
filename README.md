# Finance Tracker Backend

A robust backend API for the Finance Tracker application, built with **FastAPI** and **PostgreSQL**. This service manages user authentication, financial transactions, budgeting, and savings goals.

## 🚀 Features

- **User Authentication**: Secure JWT-based authentication.
- **Transaction Management**: Track income and expenses.
- **Budgeting**: Set and monitor storage limits.
- **Savings Goals**: Create and track progress towards financial goals.
- **Database**: Uses PostgreSQL for production and SQLite for local development/testing.
- **Migrations**: Database schema management with Alembic.

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: PostgreSQL (Production), SQLite (Dev)
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Testing**: Pytest
- **Containerization**: Docker

## 🔧 Setup & Installation

### Prerequisites

- Python 3.10+
- Docker & Docker Compose (optional)

### Local Development

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd finTrack/backend
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory (copy from example if available) and set your variables:
    ```ini
    DATABASE_URL=sqlite:///./sql_app.db
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5.  **Run Migrations:**
    ```bash
    alembic upgrade head
    ```

6.  **Start the Server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://localhost:8000`. API docs at `/docs`.

## 🐳 Docker

Run the application using Docker Compose:

```bash
docker-compose up --build
```
