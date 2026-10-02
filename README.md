# Auth API Service

FastAPI implementation for task T-2 (Auth endpoint).

## Setup & Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

3. Test POST `/api/login`:
   - Sample credentials:
     - Username: `admin`, Password: `admin123`
     - Email: `user@example.com`, Password: `user123`