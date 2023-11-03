FROM python:3.11-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY itbot itbot
COPY telegram_bot telegram_bot
COPY manage.py .

ARG TELEGRAM_BOT_TOKEN=000:
RUN python manage.py migrate

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
