FROM python:3.11-slim

RUN apt update && \
    apt install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY itbot itbot
COPY telegram_bot telegram_bot
COPY manage.py .

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
