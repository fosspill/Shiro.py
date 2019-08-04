FROM debian:buster

RUN apt-get update \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get install --no-install-recommends software-properties-common git python3-pip libpq-dev -y \
    && apt install --no-install-recommends python3.7 -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/MrSpinne/Shiro.py.git
RUN cp -a Shiro.py/. .
RUN rm -rf Shiro.py/
RUN pip3 install -r requirements.txt

ENV POSTGRES_HOST localhost
ENV POSTGRES_PORT 5432
ENV POSTGRES_DATABASE shiro
ENV POSTGRES_USER shiro
ENV POSTGRES_PASSWORD shiro
ENV LAVALINK_HOST localhost
ENV LAVALINK_PORT 2333
ENV LAVALINK_PASSWORD shiro
ENV LAVALINK_REGION eu

ENTRYPOINT ["python3", "shiro.py"]