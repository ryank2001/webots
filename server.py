

import asyncio
import json
import websockets
from aStar import aStarSearch

gridHeight = 10
gridWidth = 10
grid = [[0 for i in range(gridHeight)] for j in range(gridWidth)]
robots = {}
clones = {}
gui = {}
targets = {'MEGA RAT' : {"pos" : [9,9]}}


async def connect(json_data, websocket):
    ''' 
    This function is called when a robot tries to first connect to the server.
    It checks or the robot is a actual robot or a clone in Webots and saves the connection.

    Parameters:
        json (dict): The json data send by the robot.
        websocket (WebSocketServerProtocol): The connection to the robot.

    Returns:
        None
    '''
    try:
        id = json_data["robot_name"]
        fake = json_data["fake"]
        if fake:
            clones[id] = {'connection' : websocket}
            print("clone "+ str(id) +  " connected to the api")
        else:
            robots[id] = {'connection' : websocket}
            print("robot "+ str(id) +  " connected to the api")
            jsonData = {
                "type": "target_position",
                "robot_name": "MEGA RAT",
                "x": 4,
                "y": 12
            }
            await websocket.send(json.dumps(jsonData))
    except KeyError:
        print("invalid connect")


def calculate_path(robotName):
    '''
    This function calculates the next position for a robot to move to.

    Parameters:
        robotName (string): The name of the robot.

    Returns:
        list: The next position for the robot to move to in the form [x,y].
    '''
    currentPos = clones[robotName]["pos"]
    targetPos = targets[robotName]["pos"]

    return aStarSearch(grid, currentPos, targetPos)

    
    

async def get_robot_position(websocket, data):
    try:
        print(data)
        Name = data["robot_name"]
        obstacles = data["obstacles"]
        x = data["x"]
        y = data["y"]
        
        if websocket == clones[Name]["connection"]:
            clones[Name]["pos"] = [x,y]
            
            for obstacle in obstacles:
                print(obstacle)
                if obstacle["x"] >= 0 or obstacle["y"] >= 0:
                    if obstacle["x"] < gridWidth  and obstacle["y"] < gridHeight:
                        grid[int(obstacle["x"])][int(obstacle["y"])] = 1
            
            
            newPos = calculate_path(Name)

            jsonData = {
                "type": "target_position",
                "robot_name": Name,
                "x": newPos[0],
                "y": newPos[1]
            }
            if robots[Name] != None:
                await robots[Name]["connection"].send(json.dumps(jsonData))

            await websocket.send(json.dumps(jsonData))
    except KeyError:
        print(KeyError)
        print("invalid get_robot_position")




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
            await connect(json_data, websocket)

        elif json_data["type"] == "robot_position":
            await get_robot_position(websocket, json_data)

        elif json_data["type"] == "stop":
            for robot in robots:
                await robots[robot]["connection"].send(json.dumps({"type": "stop"}))
                
        
        


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())