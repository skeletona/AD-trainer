from channels.generic.websocket import WebsocketConsumer
from django.utils.timezone import now, timedelta
from django.db.models import Max
from core.models import Game
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
import zipfile, os

User = get_user_model()

class Consumer(WebsocketConsumer):
    ALLOWED_SERVICES = {"bluwal", "explorers", "neftetochka", "oilmarket"}

    def get_time(self):
        time = self.query_params.get("time", [""])[0]
        if not time.isdigit():
            self.send('Error in query: Time must be an integer!')
            raise TypeError('Time must be an integer: ' + time)
        elif int(time) < 10:
            self.send('Error in query: Time must be more than 10 minutes!')
            raise TypeError('Time is less then 10 minutes: ' + time)
        elif time(time) > 1440:
            self.send('Error in query: Time must be less than 24 hours!')
            raise TypeError('Time is more then 24 hours: ' + time)
        return int(time)

    def get_services(self):
        services = self.query_params.get("services", [''])[0].split(",")
        if services == ['']:
            self.send('Error in query: You must choose at least one service')
            raise ValueError('Empty service list')
        
        for i in services:
            if i.strip() not in self.ALLOWED_SERVICES:
                self.send('Error in query: No such service:', i.strip())
                raise TypeError('No such service:', i.strip())
        return services

    def connect(self):
        self.accept()
        try:
            user = self.scope['user']

            if user.is_authenticated:
                self.query_params = parse_qs(self.scope["query_string"].decode())
                time = self.get_time()
                services = self.get_services()

                self.send('Starting game...')
                now_in_minutes = now().replace(second=0, microsecond=0)
                game = Game.objects.create(
                    start=now_in_minutes,
                    duration=time,
                    end=now_in_minutes + timedelta(minutes=time),
                    services=services,
                    players=[user.username]
                )
                game_id = Game.objects.aggregate(max_id=Max('id'))['max_id']
                
                os.system(f'rm -rf "../games/{game_id}"')
                os.system(f'mkdir ../games/{game_id}')

                self.send('Creating archive...')
                with zipfile.ZipFile('test.zip', mode='w') as zf:
                    for service in services:
                        zf.write(os.path.join('../vulnbox/services', service))
                self.send('Done!')

                user.game = game
                user.save()

                os.system('docker rm --force vpn && docker compose up vpn -d')
                self.send("User game updated!")

                self.send('Success!')
            else:
                self.send("User is not authenticated!")
        except Exception as e:
            print('Error:', e, flush=True)
        finally:
            self.close()
