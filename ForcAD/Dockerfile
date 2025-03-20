FROM alpine

COPY ./images.tar /images.tar
COPY ./ForcAD /home/ForcAD
WORKDIR /home/ForcAD
RUN apk add docker docker-compose python3 py-pip
RUN pip install -r cli/requirements.txt --break-system-packages
RUN python control.py setup

CMD dockerd & sleep 2 && docker load -i /images.tar && python control.py start && tail -f /dev/null
