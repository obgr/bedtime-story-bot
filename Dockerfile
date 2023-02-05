# Run this docker file from the parent directory, see README.md
FROM python:3.10-slim-bullseye

# Upgrade container.
RUN apt-get update \
    && apt-get install -y \
        libffi-dev \
        ffmpeg \
            --no-install-recommends \
            --no-install-suggests \
    && apt-get upgrade -y \
    && apt-get autoremove \
    && apt-get autoclean \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy App
COPY app/ /bot/app/
# Copy requirements.txt
COPY requirements.txt /bot/requirements.txt

WORKDIR /bot

# Create virtual environment
RUN mkdir /bot/venv \
    && python3 -m venv /bot/venv \
    && . /bot/venv/bin/activate \
    && pip3 install -r requirements.txt

COPY docker/entrypoint.sh /bot/
RUN chmod +x /bot/entrypoint.sh
ENTRYPOINT ["/bot/entrypoint.sh"]
CMD [""]