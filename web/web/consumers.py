from channels.generic.websocket import WebsocketConsumer
from django.utils.timezone import now
from django.db.models import Max
from core.models import Game
from django.contrib.auth import get_user_model
from os import popen, system

User = get_user_model()

class Consumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        try:
            self.send('Starting game...')
            user = self.scope['user']

            if user.is_authenticated:
                system('docker rm --force vpn && docker compose up vpn -d')
                game = Game.objects.create(
                    start=now(),
                    duration=540,  # 9 часов
                    services=["bluwal", "explorers", "neftetochka", "oilmarket"],
                    players=[user.username]
                )
                game_id = Game.objects.aggregate(max_id=Max('id'))['max_id']
                
                system(f'rm -rf "../games/{game_id}"')
                system(f'mkdir ../games/{game_id}')

                self.send('Creating archive...')
                system(f'7z a ../games/{game_id}/services.7z ../games/{game_id}/* {" ".join(map(lambda x: "../vulnbox/services/" + x, game.services))} > /dev/null')
                self.send('Done!')

                user.game = game
                user.save()
                self.send("User game updated!")

                self.send('Success!')
            else:
                self.send("User is not authenticated!")

        except Exception as e:
            print("Error:", e)
        finally:
            self.close()
