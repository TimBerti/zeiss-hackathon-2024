import asyncio
import websockets
import random
import json

async def send_random_numbers(websocket, path):
    while True:
        numbers = [random.randint(0,1) for _ in range(9)]
        await websocket.send(json.dumps(numbers))
        await asyncio.sleep(1)

start_server = websockets.serve(send_random_numbers, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
