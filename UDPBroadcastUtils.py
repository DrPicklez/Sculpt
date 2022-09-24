from asyncio.subprocess import DEVNULL
import socket
import threading
from time import sleep
import os
import subprocess
import pathlib


class Networking():

    def __init__(self, broadcastInfoPort):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.myIp = socket.gethostbyname(socket.gethostname())
        self.infoPort = broadcastInfoPort
        self.t_stop = threading.Event()
        self.serverThread = threading.Thread(target=self.sendPortInformation, args=(self.t_stop,))
        self.serverThread.daemon = True
        self.imageServerPath = os.path.abspath(os.getcwd())
        #print("myIp Is: " + self.myIp)
        #        
    def scanNetworkForHandShake(self):
        message = "ARE_YOU_BABBLE"
        self.sendHostIsAlive()
        devices = subprocess.check_output(["arp", "-a"])
        devices = devices.decode("utf-8")
        devices = devices.splitlines()
        devices = devices[3:]
        _devices = []

        for device in devices:
            ip, mac, dhcp = device.split()
            r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            myNetwork = socket.gethostbyname(socket.gethostname())
            if(ip.split(".")[0] == self.myIp.split(".")[0] and (ip.split(".")[-1] != "255")):    #check for same network (192.*) AND is not boradcast (192.*.255)
                r.bind((myNetwork,self.infoPort))
                print("tryingToConnectTo: " + str(ip))
                self.sock.sendto(message.encode(), (ip, self.infoPort))
                r.settimeout(0.5)   #wait timout for handshake
                try:
                    data, adress = r.recvfrom(1024)
                    data = data.split(b'-EOM')[0]
                    data = data.decode("utf-8")
                    data.split(":")
                    _devices.append(adress[0])
                    print(data)
                except socket.timeout as e:       
                    print("notBable")
            r.close()
        
        return _devices
    
    def setImageServerPort(self, imageServerPort):
        self.imageServerPort = imageServerPort
    
    def sendIsAlive(self):
        self.sock.sendto(bytes("I_AM_BABLE_HOST-" + str(self.infoPort) + "-EOM", "utf-8"), ("192.168.0.255", self.infoPort))

    def setControlServerPort(self, webSocketPort):
        self.websocketPort = webSocketPort

    def getMacFromIP(self, ipAdresses):
        _devices = []
        for ips in ipAdresses:
            device = subprocess.check_output(["arp", "-a", str(ips)])
            device = device.decode("utf-8")
            device = device.splitlines()
            #device = device[3:]
            ip, mac, dhcp = device[3].split()
            _devices.append((ip, mac))
        return _devices


    def sendPortInformation(self, stop_event):
        while(not stop_event.is_set()):
            if(self.imageServerPort is not None):
                self.sock.sendto(bytes("I_AM_BABLE_IMAGE_SERVER-" + str(self.imageServerPort) + "-EOM", "utf-8"), ("192.168.0.255", self.infoPort))
            if(self.websocketPort is not None):
                self.sock.sendto(bytes("I_AM_BABLE_CONTROL_SERVER-" + str(self.websocketPort) + "-EOM", "utf-8"), ("192.168.0.255", self.infoPort))
            stop_event.wait(5)

    def startPortInfoSender(self):
        self.serverThread.start()
    
    def stopPortInfoSender(self):
        self.t_stop.set()
        self.serverThread.join()
    

    def setupBableNumbers(self, devices):
        message = "YOU_ARE_BABBLE_NUMBER-"
        _devices = []

        for babbleNumber, ip in enumerate(devices):
            r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            myNetwork = socket.gethostbyname(socket.gethostname())
            r.bind((myNetwork,self.infoPort))
            print("requestingEnunerationFrom: " + "toBeNumber: " + str(babbleNumber))
            message += (str(babbleNumber) + " -EOM")
            self.sock.sendto(message.encode(), (ip, self.infoPort))
            #r.settimeout(0.5)   #wait timout for handshake
            try:
                zata, adress = r.recvfrom(1024)
                data = zata.split(b'-EOM')[0]
                data = data.decode("utf-8")
                data.split(":")
                _devices.append((adress[0], babbleNumber))
                print(data)
            except socket.timeout as e:       
                print("BadIPRequestedForEnumeration")
            r.close()

            return _devices

    def closeSocket(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        print('ClosingHostSocket!')
        
