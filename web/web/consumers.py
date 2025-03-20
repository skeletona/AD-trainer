from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import subprocess

class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.process = None
        self.is_active = True

        try:
            self.process = await asyncio.create_subprocess_exec(
                '../restart.sh',
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )

            while self.is_active and self.process.returncode is None:
                data = await self.process.stdout.readline()
                if not data:
                    break
                await self.send(data.decode().strip())
            
        finally:
            if self.process and self.process.returncode is None:
                self.process.terminate()
            await self.close()

    async def disconnect(self, close_code):
        self.is_active = False
        if self.process and self.process.returncode is None:
            self.process.terminate()