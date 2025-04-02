from channels.generic.websocket import WebsocketConsumer
from django.utils.timezone import now, timedelta
from django.db.models import Max
from core.models import Game
from django.contrib.auth import get_user_model
from os import system

User = get_user_model()

class Consumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        try:
            self.send('Starting game...')
            user = self.scope['user']

            if user.is_authenticated:
                system('docker rm --force vpn && docker compose up vpn -d')
                now_in_minutes = now().replace(second=0, microsecond=0)
                minutes = 540  # 9 часов
                game = Game.objects.create(
                    start=now_in_minutes,
                    duration=minutes,
                    end=now_in_minutes + timedelta(minutes=minutes),
                    services=["bluwal", "explorers", "neftetochka", "oilmarket"],
                    players=[user.username]
                )
                game_id = Game.objects.aggregate(max_id=Max('id'))['max_id']
                
                system(f'rm -rf "../games/{game_id}"')
                system(f'mkdir ../games/{game_id}')

                self.send('Creating archive...')
                system(f'7z a -r ../games/{game_id}/services.7z ../games/{game_id}/* ../vulnbox/services/" > /dev/null')
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
