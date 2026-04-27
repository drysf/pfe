FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        netcat-openbsd curl fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY scripts/requirements.txt /app/scripts/requirements.txt
RUN pip install --no-cache-dir -r /app/scripts/requirements.txt

COPY scripts/ /app/scripts/

WORKDIR /app/scripts
RUN python generate_assets.py

EXPOSE 5000 4242
CMD ["python", "orchestrator.py"]
