FROM debian:bookworm-slim

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y openjdk-17-jre-headless \
                       unzip curl procps vim net-tools \
                       python3 python3-pip python3.11-venv

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

RUN mkdir gateway && cd gateway && \
    curl -O https://download2.interactivebrokers.com/portal/clientportal.gw.zip && \
    unzip clientportal.gw.zip && rm clientportal.gw.zip

COPY conf.yaml gateway/root/conf.yaml
COPY start.sh /app

COPY pyproject.toml README.md /app/
COPY src /app/src
COPY scripts /app/scripts
COPY webapp /app/webapp

EXPOSE 5055 5056

CMD sh ./start.sh
