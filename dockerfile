FROM python:3-alpine

LABEL org.opencontainers.image.source https://github.com/thetanz/ransomwatch

COPY *.py /
COPY *.json /
COPY assets/ /assets/
COPY requirements.txt /requirements.txt

RUN apk update
RUN apk upgrade
RUN apk add --no-cache g++ gcc libxml2-dev libxslt-dev libffi-dev openssl-dev make curl jq firefox-esr

RUN curl -L `curl -sL https://api.github.com/repos/mozilla/geckodriver/releases/latest | jq -r '.assets[].browser_download_url' | grep 'linux64.tar.gz$'` | tar -xz
RUN chmod +x geckodriver
RUN mv geckodriver /usr/local/bin

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "ransomwatch.py"]