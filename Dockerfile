FROM python:3.6.4-alpine3.7

COPY replacer.py /opt/

ENTRYPOINT [ "python", "/opt/replacer.py" ]

