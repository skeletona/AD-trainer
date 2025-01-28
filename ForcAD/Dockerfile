FROM debian

COPY ./docker-compose /usr/lib/docker/cli-plugins/docker-compose
COPY ./images.tar /images.tar
COPY ./ForcAD /home/ForcAD
WORKDIR /home/ForcAD

RUN apt update && apt install -y docker.io python3-venv
RUN dockerd & sleep 2 && docker load -i /images.tar && rm /images.tar

CMD dockerd & sleep 2 && /venv/bin/python control.py start && tail -f /dev/null
