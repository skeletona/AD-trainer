#!/bin/bash
set -euo pipefail
cd $(dirname "$BASH_SOURCE")

R=$(tput setaf 1)
G=$(tput setaf 2)
B=$(tput setaf 3)
Z=$(tput sgr0)

# build ForcAD
if [ ! -f ForcAD/images.tar ]; then
	echo "${B}Looks like ForcAD containers are not built! Building Forcad ^_^${Z}"
	cd ForcAD/ForcAD
	cp ../forcad_config.yml config.yml
	docker compose build
	docker save -o ../images.tar forcad-flower forcad-celery forcad-events forcad-admin-api forcad-http-receiver forcad-client-api forcad-ticker forcad-initializer forcad-nginx postgres rabbitmq redis
	cd ../../
	echo "${G}ForcAD built!${Z}"
fi

# build services
if [ ! -f vulnbox/tmp/images.tar ]; then
	echo "${B}Looks like services for vulnbox are not built! Building services ^_^${Z}"
	cd vulnbox/services
	for service in ./*;	do
	docker-compose -f $service/docker-compose.yml pull
	docker-compose -f $service/docker-compose.yml build
	done
	cd ../../
	docker save -o vulnbox/tmp/images.tar neftetochka-app explorers-app oilmarket-app bluwal-bluwal bluwal-app mongo:7.0.2 postgres:14 nginx:1.25-alpine golang:1.21-alpine caddy:2.7.5-alpine python:3.11-slim-bullseye ubuntu:22.04 rust:1.73-bookworm
	echo "${G}services built!${Z}"
fi

echo "${R}Deleting containers...${Z}"
docker rm --force forcad vulnbox vpn

echo "${R}Deleting network...${Z}"
docker network rm game || true

echo "${G}Starting simulation...${R}"
docker compose up -d --build

echo "${R}Deleting unused images${Z}"
docker rmi $(docker images -f "dangling=true" -q) | grep -v "sha256"

echo "${G}ALL DONE! Go to http://185.185.26.128:8888 to get your OVPN config!${Z}"
