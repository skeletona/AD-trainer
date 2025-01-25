#!/bin/bash

R=$(tput setaf 1)
G=$(tput setaf 2)
B=$(tput setaf 4)
Z=$(tput sgr0)

echo "${R}Stopping containers...${Z}"
docker stop -t 0 player game

echo "${R}Deleting containers...${Z}"
docker rm game-player game

echo "${R}Deleting image...${Z}"
docker rmi game-main_container | grep -v "sha256"

echo "${B}Starting container...${R}"
docker compose up -d --build

echo "${G}Go to http://62.173.146.31:8000 to get your OVPN config!${Z}"
