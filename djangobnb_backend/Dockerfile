FROM python:3.11-slim

WORKDIR /usr/src/airbnb_backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat-openbsd

# Install system dependencies: libpq-dev and gcc for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements file and install Python dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/airbnb_backend/entrypoint.sh
RUN chmod +x /usr/src/airbnb_backend/entrypoint.sh

# Copy the rest of the application code
COPY . .

ENTRYPOINT ["/usr/src/airbnb_backend/entrypoint.sh"]