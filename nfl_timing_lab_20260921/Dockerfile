FROM python:3.12-slim
WORKDIR /app
COPY collector /app/collector
RUN mkdir /data
VOLUME ["/data"]
CMD ["python", "-u", "collector/record.py", "--panel", "collector/development_panel.json", "--database", "/data/capture.sqlite", "--seconds", "86400"]
