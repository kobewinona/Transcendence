FROM python:3.11

LABEL org.opencontainers.image.authors="Lera, Dima, Wolf, Jeremy"

WORKDIR /usr/src/app

# переменные окружения для python
#prevents Python from generating .pyc files
#ensures Python output is sent straight to terminal without buffering
ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
RUN mkdir -p /usr/src/app/static

EXPOSE 8000

# RUN python manage.py collectstatic --noinput
# Start Daphne server
#moved the database operations (migrations) from build time to runtime!!!!(bacause network did not created yet)
CMD sh -c "python3 manage.py makemigrations --noinput && \
           python3 manage.py migrate --noinput && \
           python3 manage.py collectstatic --noinput && \
           daphne -b 0.0.0.0 -p 8000 project.asgi:application"


# FROM python:3.11

# LABEL org.opencontainers.image.authors="Lera, Dima, Wolf, Jeremy"

# WORKDIR /usr/src/app

# # Install dependencies
# COPY requirements.txt .
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# # Copy project files
# COPY . .

# # Create STATIC_ROOT directory
# RUN mkdir -p /usr/src/app/staticfiles

# # Collect static files
# RUN python manage.py collectstatic --noinput

# # Apply migrations
# RUN python manage.py makemigrations --noinput
# RUN python manage.py migrate --noinput

# # Start Daphne server
# CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "project.asgi:application"]