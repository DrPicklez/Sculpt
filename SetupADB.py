from os import sep
from signal import default_int_handler
import subprocess
import os
import time
from UDPBroadcastUtils import Networking

UDP_BROADCAST_PORT = 50008
#UDP_BROADCAST_PORT = 5005

class AdbControl():
    def __init__(self):
        self.networkUtils = Networking(UDP_BROADCAST_PORT)
        pass

    def scanNetwork(self):
        i = 0
        #while i < 10:
        self.networkUtils.sendIsAlive()
        time.sleep(5)
         #   i += 1
        
        
        devices = subprocess.check_output(["arp", "-a"])
        devices = devices.decode("utf-8")
        devices = devices.splitlines()
        devices = devices[3:]
        
        _devices = []
        for device in devices:
            ip, mac, dhcp = device.split()
            _devices.append((ip, mac, dhcp))
        
        return _devices
    
    def connectDevices(self, devices):
        for device in devices:
            ip, mac, dhcp = device
            ip += ":5555"
            subprocess.run(["adb", "connect", ip], capture_output=True)

    def getConnectedDevices(self):
        devices = subprocess.check_output(["adb", "devices"])
        devices = devices.decode("utf-8")
        devices = devices.splitlines()
        devices = devices[:-1]
        del devices[0]
        _devices = []
        for device in devices:
            ip, device = device.split(sep='\t')
            if(device == 'device'):
               ip, port = ip.split(sep=':')
               print("connected:" + ip + ":" + port)
               _devices.append((ip, port))
        return _devices


    def updateDevices(self, devices):
        _updatedDevices = []
        tStart = time.time()
        subprocess.run(["adb", "disconnect"], capture_output=True, text=True)   #safety disconnect from all dangling devices
        for device in devices:
            ip, mac, dhcp = device
            ip += ":5555"
            
            result = subprocess.run(["adb", "connect", ip], capture_output=True, text=True)
            if(result.stdout.find("connected to ") != -1):
                print(result.stdout.strip("\n"))

            updateResult = subprocess.run(["adb", "install", "-r", "-g", self.getAPKLocation()], capture_output=True, text=True)
            if(updateResult.stdout.find("Success") != -1):
                updatedIP = result.stdout.strip("\n")
                updatedIP = updatedIP.strip("connected to ")
                _updatedDevices.append(updatedIP)
                print("UpdatedDevice")

            result = subprocess.run(["adb", "disconnect", ip], capture_output=True, text=True)
            if(result.stdout.find("disconnected ") != -1):
                print(result.stdout.strip("\n"))
                print("")
            
        timeTaken = time.time() - tStart
        print("it took: " + str(timeTaken) + " seconds") 
        print("to update: " + str(len(_updatedDevices)) + " devices")
        return _updatedDevices
    
    def getConnectedADBDevices(self, devices):
        _connectedDevices = []
        tStart = time.time()
        subprocess.run(["adb", "disconnect"], capture_output=True, text=True)   #safety disconnect from all dangling devices
        for device in devices:
            ip, mac, dhcp = device
            ip += ":5555"
            
            result = subprocess.run(["adb", "connect", ip], capture_output=True, text=True)
            if(result.stdout.find("connected to ") != -1):
                print(result.stdout.strip("\n"))
                connection = result.stdout.strip("connected to ")
                ip, port = connection.split(":")
                _connectedDevices.append(ip)

            result = subprocess.run(["adb", "disconnect", ip], capture_output=True, text=True)
            if(result.stdout.find("disconnected ") != -1):
                print(result.stdout.strip("\n"))
                print("")
            
        timeTaken = time.time() - tStart
        print("it took: " + str(timeTaken) + " seconds to scan for ADB Devices") 
        print("There are: " + str(len(_connectedDevices)) + "ADB Devices Connected")
        return _connectedDevices

    def getAPKLocation(self):
        path = os.getcwd()
        master = "UE5_TowerOfBabel_Physical"
        dir, path = path.split(master)
        dir += master + "\Builds\\Android\\UE5_TowerOfBabel_Physical-arm64.apk"
        return dir

#path = os.path.join(path, os.pardir)

androidManager = AdbControl()
devices = androidManager.scanNetwork()
#devices = androidManager.getConnectedADBDevices(devices)
print(androidManager.updateDevices(devices))


#androidManager.connectDevices(devices)

#androidManager.installAPK(connectedDevices)


