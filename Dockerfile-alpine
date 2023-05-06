FROM ruby:alpine

LABEL maintainer="Eero Virta <eero.virta@patreon.me>"

RUN apk update && apk add --no-cache python3 py3-pip \
        && pip install json-spec \
        && pip install publicsuffix \
        && gem install whois \
        && gem install whois-parser

VOLUME /tmp
WORKDIR /tmp

COPY entrypoint.sh /entrypoint.sh
COPY crontab /etc/crontabs/root
COPY domlist.py test.rb /opt/

ENTRYPOINT ["/entrypoint.sh"]
CMD [ "crond", "-f", "-d", "8"]

