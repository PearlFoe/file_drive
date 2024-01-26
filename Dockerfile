FROM python:3.11-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . .

ARG UID=10001
ARG USER="user"

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/${USER}" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    ${USER}

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

USER ${USER}

EXPOSE 8000

CMD ["gunicorn", "app:get_app", "--chdir", "/app/src/server/", "--bind", "localhost:8080", "--worker-class", "aiohttp.GunicornWebWorker"]
