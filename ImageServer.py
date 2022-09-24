import subprocess
import os
from asyncio.subprocess import DEVNULL
import socket
import time 
from os import listdir
from os.path import isfile, join

class ImageServer:

    def __init__(self, serverPort):
        self.imageServerPath = os.path.abspath(os.getcwd())
        self.imageServerPath += "\Images"
        self.imageServerPort = serverPort
        self.myIp = socket.gethostbyname(socket.gethostname())
        self.colorNamePrefix = "T_Facade_"
        self.colorNameSufix = "_BC"
        self.depthNameSufix = "_RMD"
        pass

    def setImageServerPort(self, imageServerPort):
        self.imageServerPort = imageServerPort

#http://10.12.1.180:5097/Color/T_Facade_0_BC.png
    def getColorURL(self, n):
        url = "http://" + self.myIp + ":" + str(self.imageServerPort) + "/Color/"
        url += self.colorNamePrefix
        url += str(n)
        url += self.colorNameSufix
        url += ".png"
        return url
    
    def getDepthURL(self, n):
        url = "http://" + self.myIp + ":" + str(self.imageServerPort) + "/Depth/"
        url += self.colorNamePrefix
        url += str(n)
        url += self.depthNameSufix
        url += ".png"
        return url

    def shareFolder(self):
        print(self.imageServerPath)
        cmd = "python -m http.server --bind " + self.myIp + " --directory " + self.imageServerPath + " " + str(self.imageServerPort)
        print(cmd)
        self.process = subprocess.Popen("python -m http.server --bind " + self.myIp + " --directory " + self.imageServerPath + " " + str(self.imageServerPort),
                        shell=False, 
                        stdout=subprocess.PIPE,
                        stderr=DEVNULL)
        self.process

#imServ = ImageServer(5097)
#imServ.shareFolder()
#print(imServ.getColorURL(0))
#print(imServ.getDepthURL(0))
#time.sleep(500)