FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["gunicorn", "askme_koshenkov.wsgi:application", "-w", "2", "--bind", "0.0.0.0:8081"]