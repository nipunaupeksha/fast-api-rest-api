# Use an official Python image as a base
FROM python:3.11-slim

# Environment variables
ENV SECRET_KEY nipunaupeksha
ENV ACCESS_TOKEN_EXPIRE_MINUTES 38
ENV DATABASE_USER postgres
ENV DATABASE_PASSWORD postgres
ENV DATABASE_HOST localhost
ENV DATABASE_PORT 5432
ENV DATABASE_NAME adastra_db
ENV ADMIN_EMAIL admin@email.com
ENV ADMIN_PASSWORD admin123
ENV ADMIN_USERNAME admin

# Set environment variables to prevent Python from writing .pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /app

# Copy Poetry configuration files
COPY pyproject.toml /app
COPY poetry.lock /app

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application code
COPY ./rest_api_project /app

# Copy the .env file
COPY .env /app/.env

# Expose port 8000 to allow access to the FastAPI application
EXPOSE 8000

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
