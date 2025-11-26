# Dockerfile - FastAPI app
FROM python:3.11-slim

# set working dir
WORKDIR /app

# system deps (if you need build tools, uncomment)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# copy code (in Jenkins pipeline the host workspace will be volume-mounted over /app)
COPY . /app

EXPOSE 8000

# default command (use uvicorn)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

