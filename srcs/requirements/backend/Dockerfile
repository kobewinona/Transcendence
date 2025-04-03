# BASE IMAGE & AUTHOR INFORMATION
FROM python:3.12

LABEL org.opencontainers.image.authors="Dima, Wolf, Jeremy"

# SET WORKING DIRECTORY
WORKDIR /usr/src/app

# INSTALL SYSTEM DEPENDENCIES
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    supervisor \
    lsof && \
    rm -rf /var/lib/apt/lists/*

# INSTALL PIPENV FOR MANAGING PYTHON DEPENDENCIES
RUN pip install --upgrade pip && pip install pipenv

# COPY DEPENDENCY FILES FIRST (CACHING LAYER)
COPY Pipfile Pipfile.lock ./

# INSTALL PYTHON DEPENDENCIES USING PIPENV
ARG DEV_MODE=false
RUN if [ "$DEV_MODE" = "true" ]; then \
        pipenv install --deploy --ignore-pipfile --dev; \
    else \
        pipenv install --deploy --ignore-pipfile; \
    fi

# COPY PROJECT FILES
COPY . .

# STATIC FILES CONFIGURATION
RUN mkdir -p /usr/src/app/staticfiles

# SET EXECUTION PERMISSIONS FOR ENTRYPOINT
RUN chmod +x /usr/src/app/tools/entrypoint.sh

# ENTRYPOINT & SUPERVISOR CONFIGURATION
ENTRYPOINT ["/usr/src/app/tools/entrypoint.sh"]
COPY ./conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./conf/supervisord.dev.conf /etc/supervisor/conf.d/supervisord.dev.conf
ENV SUPERVISOR_CONF_PATH="/etc/supervisor/conf.d/supervisord.conf"
RUN mkdir -p /usr/src/app/logs
CMD ["sh", "-c", "supervisord -c $SUPERVISOR_CONF_PATH"]
