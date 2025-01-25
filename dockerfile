FROM python:3.11-slim


WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

COPY . /app/

RUN chmod +x /app/start.sh
