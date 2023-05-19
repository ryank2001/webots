

import asyncio
import json
import websockets

grid = [[0 for i in range(10)] for j in range(10)]
robots = {}
clones = {}
gui = {}
targets = {}

def connect(json, websocket):
    try:
        id = json["robot_name"]
        fake = json["fake"]
        if fake:
            clones[id] = {'connection' : websocket}
            print("clone "+ str(id) +  " connected to the api")
        else:
            robots[id] = {'connection' : websocket}
            print("robot "+ str(id) +  " connected to the api")'
    except KeyError:
        print("invalid connect")

def get_robot_position(websocket, data):
    try:

def calculate_path():


async def handler(websocket):
    print("new connection")
    while True:
        try:
            message = await websocket.recv()
        except websockets.exceptions.ConnectionClosedOK:
            print("connection closed")
            break
        json_data = json.loads(message)
       

        if json_data["type"] == "connect":
            connect(json_data, websocket)

        elif json_data["type"] == "robot_position":
            try:
                id = json_data["robot_name"]
                if websocket == clones[id]["connection"]:
                    clones[id]["x"] = json_data["x"]
                    clones[id]["y"] = json_data["y"]
                    print("robot "+ str(id) +  " is at position " + str(json_data["x"]) + "," + str(json_data["y"]))
        
            except KeyError:
                print("robot "+ str(id) +  " not connected to the api")
            

        elif json_data["type"] == "stop":
            for robot in robots:
                robot["connection"].send(json.dumps({"type": "stop"}))
        
        await websocket.send(message)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())