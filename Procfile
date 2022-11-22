// web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
// web: gunicorn main:app --reload
// web: uvicorn src.main:app --host=0.0.0.0 --port=${PORT:-5000}
web: uvicorn main:app --reload --host=0.0.0.0 --port=$PORT --no-browser