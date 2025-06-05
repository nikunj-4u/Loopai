# LoopAI - Data Ingestion API

This is a FastAPI-based microservice designed for data ingestion as part of the LoopAI system.

## Features

- RESTful API built using FastAPI
- Modular and lightweight
- Ready for deployment with `uvicorn`

## Project Structure

```
LoopAI/
└── data-ingestion-api/
    ├── main.py               # Entry point for the FastAPI app
    ├── requirements.txt      # Python dependencies
    └── venv/                 # Local virtual environment (not recommended for version control)
```

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd LoopAI/data-ingestion-api
```

### 2. Set Up Environment

Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
uvicorn main:app --reload
```

Access the API at: [http://localhost:8000](http://localhost:8000)

