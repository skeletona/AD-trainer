FROM alpine

COPY ./images.tar /images.tar
WORKDIR /home/ForcAD
RUN apk add docker docker-compose python3
COPY ./ForcAD /home/ForcAD

CMD dockerd & sleep 2 && docker load -i /images.tar && ./bin/python control.py start && tail -f /dev/null
