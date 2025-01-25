mkdir /var/run/sshd
echo "root:pass" | chpasswd
echo "PermitRootLogin yes
PasswordAuthentication yes" >> /etc/ssh/sshd_config
chsh -s /usr/bin/fish root
hostname player
echo "alias ip \"ip -c=auto\"
cd /home" > /etc/fish/config.fish
fish -c 'set -U fish_greeting ""'

if [ -f /tmp/images.tar ]; then
	docker load -i /tmp/images.tar
	rm -f /tmp/images.tar
fi

for service in /home/services/*; do
	docker compose -f $service/docker-compose.yml create;
done
