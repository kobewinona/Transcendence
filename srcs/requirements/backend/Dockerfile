FROM python:3.13

LABEL org.opencontainers.image.authors="Lera, Dima, Wolf, Jeremy"

WORKDIR /usr/src/app

# переменные окружения для python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Create STATIC_ROOT directory
RUN mkdir -p /usr/src/app/static/staticfiles
# Collect static files
# RUN python manage.py collectstatic --noinput

# Apply migrations
# RUN python manage.py makemigrations --noinput
# RUN python manage.py migrate --noinput
EXPOSE 8000
# Start Daphne server
# CMD sh -c "python3 manage.py makemigrations && \
#            python3 manage.py migrate && \
#            python3 manage.py collectstatic --noinput && \
#            python3 manage.py runserver 0.0.0.0:8000"
# CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "project.asgi:application"] 
CMD sh -c "python3 manage.py makemigrations --noinput && \
           python3 manage.py migrate --noinput && \
           python3 manage.py collectstatic --noinput && \
           daphne -b 0.0.0.0 -p 8000 project.asgi:application"