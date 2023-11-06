FROM python:3.11-bookworm

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY itbot itbot
COPY telegram_bot telegram_bot
COPY manage.py .

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
