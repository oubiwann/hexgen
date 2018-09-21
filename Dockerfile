FROM python:3.5-slim-stretch

WORKDIR /hexgen
COPY . .

RUN apt-get update -y && \
    apt-get install -y build-essential python3-dev fonts-freefont-ttf && \
    pip install -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["./bin/hexgen"]

