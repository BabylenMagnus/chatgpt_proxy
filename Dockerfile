FROM python:3.9

WORKDIR /app

COPY . /app

RUN python3 -m pip install fastapi uvicorn[standard] httpx gunicorn

EXPOSE 9000

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9000", "--workers", "1", "--timeout", "0", "-k", "uvicorn.workers.UvicornWorker", "app.webservice:app"]
