FROM python:3.7-stretch

ADD ./requirements.txt /tmp
RUN pip install --requirement /tmp/requirements.txt

WORKDIR /src

ADD ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]