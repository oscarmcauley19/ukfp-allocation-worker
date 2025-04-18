# ukfp-allocation-worker
Celery worker service for the UKFP Deanery Allocation simulator.

# Install dependencies
```
python -m venv venv  # optional, to create a virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt
```

# Run the worker
```
uvicorn main:app --host 0.0.0.0 --port 5000
```