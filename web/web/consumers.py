from channels.generic.websocket import WebsocketConsumer
from django.utils.timezone import now
from django.db.models import Max
from .models import Game
from os import popen, system

class Consumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        try:
            self.send('Starting game...')
            system('docker rm --force vpn && docker compose up vpn -d')
            game = Game.objects.create(
                start=now(),
                duration=540,  # 9 часов
                services=["bluwal", "explorers", "neftetochka", "oilmarket"],
                players=["user1"] #TODO
            )
            game_id = Game.objects.aggregate(max_id=Max('id'))['max_id']
            system(f'mkdir ../games/{game_id}')

            self.send('Generating VPN configs...')
            for i in range(3):
                system('docker exec -d vpn ./genclient.sh')
            configs = popen('docker exec vpn ./listconfigs.sh').read().strip().split('\n')
            for i, vpn_id in enumerate(configs):
                system(f'docker exec vpn /opt/Dockovpn/getconfig.sh {vpn_id} > ../games/{game_id}/{i}.ovpn')
            self.send('Done!')

            self.send('Creating archive...')
            system(f'7z a ../games/{game_id}/services.7z ../games/{game_id}/* {" ".join(map(lambda x: "../vulnbox/services/" + x, game.services))} ')
            self.send('Done!')

            self.send('Success!')

        except Exception as e:
            print("Error:", e)
        finally:
            self.close()