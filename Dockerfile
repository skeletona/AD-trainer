FROM debian

RUN apt update && apt install -y docker.io fish nano vim curl openssh-server htop netcat-traditional neofetch
WORKDIR /home

COPY ./docker-compose /usr/lib/docker/cli-plugins/docker-compose
COPY ./services /home/services
COPY ./motd /etc/motd
COPY ./tmp /tmp

RUN dockerd & sleep 2 && /tmp/prepare.sh
CMD /tmp/entrypoint.sh
