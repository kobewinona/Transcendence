FROM python:3.12

LABEL org.opencontainers.image.authors="Dima, Wolf, Jeremy"

WORKDIR /usr/src/app

# Install system dependencies first
RUN apt-get update && apt-get install -y netcat-openbsd supervisor lsof && rm -rf /var/lib/apt/lists/*

# Install Pipenv separately to improve caching
RUN pip install --upgrade pip && pip install pipenv

# Copy dependency files first for better Docker caching
COPY Pipfile Pipfile.lock ./

# If we are only locking, then stop here
ARG LOCK_ONLY=false
RUN if [ "$LOCK_ONLY" = "true" ]; then pipenv lock && exit 0; fi

# Install dependencies using Pipenv
ARG DEV_MODE=false
RUN if [ "$DEV_MODE" = "true" ]; then pipenv install --deploy --ignore-pipfile --dev; else pipenv install --deploy --ignore-pipfile; fi

# Copy the rest of the project files
COPY . .

# Create STATIC_ROOT directory
RUN mkdir -p /usr/src/app/staticfiles
RUN pipenv run python manage.py collectstatic --noinput

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

COPY ./conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
