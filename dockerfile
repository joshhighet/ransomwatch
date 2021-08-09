FROM python:3-alpine
LABEL org.opencontainers.image.source https://github.com/thetanz/ransomwatch

COPY * /
RUN apk add --update --no-cache g++ gcc libxml2-dev libxslt-dev libffi-dev openssl-dev make

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "ransomwatch.py"]