

import asyncio
import json
import websockets

grid = [[0 for i in range(10)] for j in range(10)]
robots = {}
targets = {}

async def handler(websocket):
    while True:
        try:
            message = await websocket.recv()
        except websockets.exceptions.ConnectionClosedOK:
            print("connection closed")
            break
        json_data = json.loads(message)
       

        if json_data["type"] == "connect":
            id = json_data["robot_id"]
            robots[id]["connection"] = websocket
            print("robot "+ str(id) +  " connected to the api")

        elif json_data["type"] == "position":
            id = json_data["robot_id"]
            robots[id]["x"] = json_data["x"]
            robots[id]["y"] = json_data["y"]
            print("robot "+ str(id) +  " is at position " + json_data["x"] + " " + json_data["y"])

        elif json_data["type"] == "stop":
            for robot in robots:
                robot["connection"].send(json.dumps({"type": "stop"}))
        
        await websocket.send(message)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())