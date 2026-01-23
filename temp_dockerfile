FROM python:3.10-slim

LABEL maintainer="ritamrakshit33@gmail.com"
LABEL description="hospital-readmisson-api"


WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
