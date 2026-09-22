FROM python:3.12-slim
WORKDIR /app
COPY allowlist.py identity.py panel.py record.py admit.py resolve_event_tickers.py \
     development_panel.json prospective_panel.json /app/
RUN mkdir -p /data/development /data/prospective
VOLUME ["/data"]
# Default is the development smoke panel. Prospective admission uses
# compose.prospective.yaml and a stamped panel on the volume.
CMD ["python", "-u", "record.py", "--panel", "development_panel.json", "--database", "/data/development/capture.sqlite", "--seconds", "86400"]
