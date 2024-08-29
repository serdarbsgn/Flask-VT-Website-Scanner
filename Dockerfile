FROM python:3.10.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config supervisor \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install mysqlclient
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /var/log/supervisor \
    && touch /var/log/supervisor/supervisord.log \
    && touch /var/log/flask.out.log \
    && touch /var/log/flask.err.log \
    && touch /var/log/vt_url_scanner.out.log \
    && touch /var/log/vt_url_scanner.err.log \
    && chown -R nobody:nogroup /var/log/supervisor

EXPOSE 5000

ENV FLASK_APP=app/webapp.py

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord"]
