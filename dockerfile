FROM python:3.11-slim

RUN apt-get update && apt-get install -y cron
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

COPY . /app/

RUN chmod +x /app/start.sh

COPY cronjob /etc/cron.d/my-cron-job
RUN chmod 0644 /etc/cron.d/my-cron-job
RUN crontab /etc/cron.d/my-cron-job
CMD cron && /app/start.sh web
