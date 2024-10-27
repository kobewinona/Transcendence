FROM python:3.10

WORKDIR /app

COPY requirements.txt .
COPY ./tools/entrypoint.sh .
COPY . /app

RUN pip install -r requirements.txt
RUN chmod +x /app/tools/entrypoint.sh

EXPOSE 3000

ENTRYPOINT ["/app/tools/entrypoint.sh"]
