ARG BUILD_FROM=ghcr.io/home-assistant/base:3.23
FROM ${BUILD_FROM}

RUN apk add --no-cache \
    curl \
    jq \
    python3

COPY run.sh /run.sh
COPY bridge.py /bridge.py
RUN chmod a+x /run.sh

CMD ["/run.sh"]
