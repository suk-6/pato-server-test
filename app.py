import os
import time
import asyncio
import requests
import websockets
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USER1 = os.getenv("USER1")
USER2 = os.getenv("USER2")

matchingStartURL = f"{BASE_URL}/matching/start"


def user1Matching():
    user1Matching = requests.get(
        matchingStartURL, headers={"Authorization": f"Bearer {USER1}"}
    )
    print("User 1 Waiting start: ", user1Matching.json())


async def socket():
    async with websockets.connect(
        f"{BASE_URL.replace('http', 'ws')}/matching/waiting",
        extra_headers={"authorization": f"Bearer {USER1}"},
    ) as websocket:
        user2Matching = requests.get(
            matchingStartURL, headers={"Authorization": f"Bearer {USER2}"}
        )
        print("User 2 Waiting start: ", user2Matching.json())
        response = await websocket.recv()
        print("< {}".format(response))


for i in range(30):
    print(f"Matching {i+1} times")
    user1Matching()
    time.sleep(1)
    asyncio.get_event_loop().run_until_complete(socket())
    print()
