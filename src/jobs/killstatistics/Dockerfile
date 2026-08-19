FROM python:3.12-slim

WORKDIR /app

# PYTHONUNBUFFERED is not optional for a Job: without it a dying container takes its logs with it.
ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["python", "-m", "src.jobs.killstatistics.main"]
