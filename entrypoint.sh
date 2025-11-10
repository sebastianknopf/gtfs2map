#!/bin/bash

echo -e "\n"
echo '[1/3] Fetching GTFS data ...'
echo $GTFS_STATIC_URL
curl -sSL $GTFS_STATIC_URL -o /data/gtfs.zip

echo -e "\n"
echo '[2/3] Converting GTFS data to GeoJSON ...'
gtfs-to-geojson --configPath /app/config/vendor/g2g/config.json

echo -e "\n"
echo '[3/3] Starting feedmap converter ...'
./venv/bin/python -m feedmap $@