FROM python:3.10

# Set the metadata for the image an author
LABEL org.opencontainers.image.authors="Lera, Dima, Wolf, Jeremy"

# Create app directory
WORKDIR /app

# Copy requirements.txt and entrypoint.sh
COPY requirements.txt .
COPY ./tools/entrypoint.sh .
COPY . /app

# Install app dependencies
RUN pip install -r requirements.txt
RUN chmod +x /app/tools/entrypoint.sh

# Expose the port 8000 for information
EXPOSE 8000

# execute the command to start the app
ENTRYPOINT ["/app/tools/entrypoint.sh"]
