# STAGE 1: Builder
FROM python:3.11-slim as builder
RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates

# STAGE 2: Final Runner
FROM n8nio/runners:latest

USER root

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

ENV CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

WORKDIR /opt/runners/task-runner-python

COPY requirements.txt .
RUN uv pip install -r requirements.txt

COPY fetch_stock.py /home/runner/fetch_stock.py
COPY Telegram-new-Message.py /home/runner/Telegram-new-Message.py

RUN chown -R runner:runner /home/runner/fetch_stock.py /home/runner/Telegram-new-Message.py && \
    chmod +x /home/runner/fetch_stock.py /home/runner/Telegram-new-Message.py && \
    chown -R runner:runner /opt/runners/task-runner-python

USER runner

ENV PATH="/home/runner/.local/bin:${PATH}"
