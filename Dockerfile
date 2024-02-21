FROM python:3.11.6-alpine3.18

ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apk update && apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt \
    && apk --purge del .build-deps

COPY . .
EXPOSE 8000

CMD ["/bin/sh", "/app/django_run.sh"]

