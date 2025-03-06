#!/bin/bash
set -euo pipefail

R=$(tput setaf 1)
G=$(tput setaf 2)
B=$(tput setaf 3)
Z=$(tput sgr0)

if [ ! -f ForcAD/images.tar ]; then
	echo "${B}Looks like ForcAD is not built! Building Forcad ^_^${Z}"
	cd ForcAD/ForcAD
	python3 -m venv ./
	./bin/pip install -r cli/requirements.txt
	cp ../forcad_config.yml config.yml
	./bin/python control.py setup
	docker compose pull
	docker compose build
	docker save -o ../images.tar forcad-flower forcad-celery forcad-events forcad-admin-api forcad-http-receiver forcad-client-api forcad-ticker forcad-initializer forcad-nginx postgres rabbitmq redis
	cd ../../
	echo "${G}ForcAD built!${Z}"
fi

echo "${R}Deleting containers...${Z}"
docker rm --force forcad vulnbox vpn

echo "${R}Deleting network...${Z}"
docker network rm game

echo "${G}Starting simulation...${R}"
docker compose up -d --build

echo "${R}Deleting unused images${Z}"
docker rmi $(docker images -f "dangling=true" -q) | grep -v "sha256"

echo "${G}ALL DONE! Go to http://62.173.146.31:8000 to get your OVPN config!${Z}"
