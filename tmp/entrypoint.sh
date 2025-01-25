dockerd & sleep 1
/usr/sbin/sshd
hostname player
docker start $(docker ps -aq)
tail -f /dev/null
