from multiprocessing import reduction
import os
#from typing_extensions import Self
#script = os.path.dirname(os.path.realpath(__file__))
#os.chdir(script)

from UDPBroadcastUtils import Networking
import asyncio
import websockets
import time
import json
# global modules and initialization

#logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)
#file_path = script + '/logColourScripts.log'
#fh = logging.FileHandler(file_path)
#fh.setLevel(logging.DEBUG) # or any level you want
#logger.addHandler(fh)


# currently assumes only one image
class WebsocketServer:

    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port
        self.lock_guard = asyncio.Lock()
        self.connectedNodes = set()
        self.enumeratedNodes = []
        self.loop = asyncio.get_event_loop()
        self.bableNumber = 0
    
    async def handler(self, websocket):
        async for message in websocket:
            
            reply = {}
            #new_msg = {"header": "None", "val": "None"}
            new_msg = json.loads(message)

            if new_msg["header"] == "CLIENT_READY":
                self.connectedNodes.add(websocket)
                if(new_msg["idNumber"] != "NOT_ASSIGNED"):
                    #self.enumeratedNodes.insert(int(new_msg["idNumber"]), websocket)
                    self.enumeratedNodes.append((int(new_msg["idNumber"]), websocket))
                print("another Added")

            else:
                print("UNKNOWN MESSAGE")


    def sendMessage(self, websocket, message):
        return self.loop.run_until_complete(self.__async__sendMessage(websocket, message))

    async def __async__sendMessage(self, websocket, message):
        try:
            await websocket.send(message)
        except websockets.ConnectionClosed:
            self.connectedNodes.remove(websocket)
            websocket.connect
            pass

    #close all needs work
    def closeAllConnections(self):
        return self.loop.run_until_complete(self.__async__closeAllConnections())

    async def __async__closeAllConnections(self):
        for websocket in self.connectedNodes:
            try:
                await websocket.close(code=1000, reason='')
                #self.connectedNodes.remove(websocket)
            except websockets.ConnectionClosed:
                #self.connectedNodes.remove(websocket)
                pass


    def broadcastMessage(self, message):
        return self.loop.run_until_complete(self.__async__broadcast(message))
    
    async def __async__broadcast(self, message):
        for websocket in self.connectedNodes.copy():
            try:
                await websocket.send(message)
            except websockets.ConnectionClosed:
                self.connectedNodes.remove(websocket)
                pass
        return self.connectedNodes


    async def main(self):
        async with websockets.serve(self.handler, self.ip, self.port):
            await asyncio.Future()  # run forever

    def run(self):
        asyncio.run(self.main())
        #async with websockets.serve(broadcast, MY_IP, 8888):
        #    await asyncio.Future()  # run forever


#logger.info("closed")