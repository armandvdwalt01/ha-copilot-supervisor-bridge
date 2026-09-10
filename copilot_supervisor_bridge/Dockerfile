ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache \
    curl \
    jq \
    python3

COPY run.sh /run.sh
COPY bridge.py /bridge.py
RUN chmod a+x /run.sh

CMD ["/run.sh"]
