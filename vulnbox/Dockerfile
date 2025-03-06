FROM debian

RUN apt update && apt install -y docker.io fish nano vim curl openssh-server htop netcat-traditional neofetch docker-compose-plugin
WORKDIR /home

COPY ../services /home/services
COPY ./motd /etc/motd
COPY ./tmp /tmp

RUN dockerd & sleep 2 && /tmp/prepare.sh
CMD /tmp/entrypoint.sh
