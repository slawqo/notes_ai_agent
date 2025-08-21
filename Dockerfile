FROM registry.access.redhat.com/ubi9/python-312:latest

USER root

WORKDIR /app
ENV PBR_VERSION=0.1.0

COPY requirements.txt setup.py setup.cfg README.rst ./
COPY notes_ai_agent/ ./notes_ai_agent/

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir . && \
    chown -R 1001:0 /app

USER 1001

ENTRYPOINT ["notes_ai_agent"]
