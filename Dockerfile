FROM python:3-alpine

RUN pip install flask --no-cache-dir && \
    addgroup -S -g 2222 poc && \
    adduser -S -u 2222 -g poc poc
    
COPY main.py GIT_* /opt/

RUN chmod 755 -R /opt

USER poc

ENV FLASK_APP=/opt/main.py

EXPOSE 5000

CMD ["/bin/sh", "-c", "python -m flask run --host=0.0.0.0"]