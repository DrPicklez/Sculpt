from http import server
from multiprocessing.resource_sharer import stop
from multiprocessing.sharedctypes import Value
from socket import socket
from tkinter.messagebox import NO
from UDPBroadcastUtils import Networking
from WebSocketServer import WebsocketServer
from ImageServer import ImageServer
import threading 
import atexit
import time
import json
import asyncio
import websockets

class BabbleInterface:
 
    def __init__(self, ip, webSocketPort, imageServerPort) -> None:
        self.server = WebsocketServer(ip, webSocketPort)
        self.serverThread = threading.Thread(target=self.initialiseServer)
        self.imageServer = ImageServer(imageServerPort)
        self.imageServer.shareFolder()
        self.serverThread.start()
        self.n = 0
        
    def initialiseServer(self):
        self.server.run()
    
    def killServer(self):
        self.server.closeAllConnections()
        self.serverThread.join()    #this is only working with ctl+c

    def getConnectedNodes(self):
        return self.server.connectedNodes
        
    def getEnumeratedNodes(self):
        return self.server.enumeratedNodes
    
    def broadcastMessage(self, message):
        return self.server.broadcastMessage(message)

    def packMessage(self, _header, _value):
        message = dict(header=_header)
        if(_value is not None):
            message.update(_value)
        
        return json.dumps(message)
        

    def setupBabbleEnumeration(self, nBable):
        self.broadcastMessage(self.packMessage("BABBLE_SETUP_ID", None))

        if(nBable is not None):
            bablesToCheck = nBable
        else: bablesToCheck = len(self.getConnectedNodes())

        n = 0        
        while n < bablesToCheck:
            scannedNode = input("NextBable: ")
            ip = scannedNode.split("_MAC_")[0]

            for node in self.getConnectedNodes():
                if(ip == node.remote_address[0]):
                    babbleID = dict(babbleId=(str(n)))
                    self.server.sendMessage(node, self.packMessage("BABBLE_ID", babbleID))
                    time.sleep(2)
                    n += 1
        
        self.server.broadcastMessage(self.packMessage("END_BABBLE_SETUP", None))
        return self.getEnumeratedNodes()
    
    def sendGlobalTime(self):
        tod = dict(globalTime=str(time.localtime()))
        message = self.packMessage("GLOBAL_TIME", tod)
        return self.broadcastMessage(message)
    
    
    def changeFacade(self, node):
        nodeId, nodeConnection = node
        facadeInfo = dict(BC_Url=self.imageServer.getColorURL(nodeId+self.n),
                            D_Url=self.imageServer.getColorURL(nodeId+self.n),
                            Transition_start=str(0),
                            Transition_time=str(0))
        
        message = self.packMessage("CHANGE_FACADE", facadeInfo)
        self.server.sendMessage(nodeConnection, message)
        


MAX_BABLE = None
UDP_BROADCAST_PORT = 5005
BABBLE_WEBSOCKET_PORT = 8080
BABBLE_IMAGE_PORT = 8008

udpManager = Networking(UDP_BROADCAST_PORT)
udpManager.setControlServerPort(BABBLE_WEBSOCKET_PORT)
udpManager.setImageServerPort(BABBLE_IMAGE_PORT)
udpManager.startPortInfoSender()

interface = BabbleInterface(udpManager.myIp, udpManager.websocketPort, udpManager.imageServerPort)

def exit_handler():
    interface.killServer    #this is only working with ctl+c
    print("killedServer")

atexit.register(exit_handler)

time.sleep(5)
#print(len(interface.setupBabbleEnumeration(None)))
#print(ids, ips)

while True:
    print("N Alive Sockets: " + str(len(interface.sendGlobalTime())))
    nodes = interface.getEnumeratedNodes()
    print("N Setup Nodes: " + str(len(nodes)))
    for node in nodes:
        interface.changeFacade(node)
        time.sleep(3)
    interface.n += 1
    interface.n %= 100

