# Hash Table Based Student Database (Flask)

A small, professional Flask web app that demonstrates CRUD operations on a student database implemented using a custom in-memory hash table with separate chaining and automatic resizing.

## Features
- Add, update, search, list, and delete students
- Custom `HashTable` (Python) with:
  - Polynomial rolling hash
  - Separate chaining for collisions
  - Automatic resize when load factor > 0.75
- Clean UI with flash messages
- Structured logging and error pages (404/500)
- Unit tests for hash table behavior (pytest)

## Project Structure
```
app.py
hashtable.py
requirements.txt
templates/
  base.html, index.html, add.html, list.html, search.html, 404.html, 500.html
static/
  style.css
tests/
  test_hashtable.py
```

## Setup
1. Python 3.10+ recommended
2. Create virtual environment (Windows PowerShell):
   ```
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration
The app reads environment variables:
- `SECRET_KEY` (default: `dev-secret-key`)
- `LOG_LEVEL` (default: `INFO`)
- `HOST` (default: `127.0.0.1`)
- `PORT` (default: `5000`)
- `FLASK_DEBUG` (default: `1`)

You can create a `.env` file in the project root to override these:
```
SECRET_KEY=change-this
LOG_LEVEL=INFO
HOST=127.0.0.1
PORT=5000
FLASK_DEBUG=1
```

## Run

### Option 1: Direct Python
```
python app.py
```
Open `http://127.0.0.1:5000`

### Option 2: Docker
Build and run with Docker Compose:
```bash
docker-compose up --build
```
Or with Docker directly:
```bash
docker build -t hash-table-student-db .
docker run -p 5000:5000 hash-table-student-db
```
Open `http://localhost:5000`

## Test
```
pytest -q
```

## Notes
- Data is in-memory and will reset on restart.
- For production, set a strong `SECRET_KEY` and run behind a real WSGI server (e.g., gunicorn) with HTTPS and persistent storage.*** End Patch```} ?>>

