FROM ubuntu:22.04

LABEL maintainer="Drys Ferhi - PFE L3B Groupe 3"
LABEL description="Escape Game Cyber - Environnement Docker"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    openssl steghide \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ../scripts/ ./scripts/
RUN pip3 install -r ./scripts/requirements.txt

# Ports exposés
EXPOSE 5000 1337

CMD ["python3", "scripts/app.py"]
