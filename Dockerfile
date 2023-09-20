FROM python:3.9-slim
LABEL maintainer="djcbell@gmail.com"
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV FLASK_APP addon_script.py
ENV FLASK_RUN_HOST 0.0.0.0

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libssl-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["flask", "run"]
