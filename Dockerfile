FROM node:22

RUN apt-get update && apt-get install -y --no-install-recommends python3-venv python3-pip && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN npm install -g gtfs-to-geojson

COPY .git/ /app/.git
RUN mkdir -p /app/src/gtfs2map

COPY pyproject.toml /app
RUN python3 -m venv venv
RUN ./venv/bin/pip install --no-cache-dir .

COPY src/ /app/src
COPY config/ /app/config
RUN ./venv/bin/pip install --no-deps .

COPY entrypoint.sh /app/entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]