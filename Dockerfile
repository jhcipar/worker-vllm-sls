FROM python:3.12-slim

COPY builder/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY src /src
RUN chmod +x /src/start.sh

CMD ["/bin/sh", "/src/start.sh"]
