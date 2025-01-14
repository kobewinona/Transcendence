FROM python:3.12

LABEL org.opencontainers.image.authors="Lera, Dima, Wolf, Jeremy"

WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Create STATIC_ROOT directory
RUN mkdir -p /usr/src/app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Apply migrations
RUN python manage.py makemigrations --noinput
RUN python manage.py migrate --noinput

# Start Daphne server
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "project.asgi:application"]
