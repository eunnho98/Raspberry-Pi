import socket
import requests
import threading
import datetime
import pygame # To play Music
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Test with Ultrasonic wave sensor
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
usleep = lambda x : time.sleep(x/1000000.0)
import datetime as dt
TP = 4
EP = 17
def getDistance():
    fDistance = 0.0
    nStartTime, nEndTime = 0, 0
    GPIO.output(TP, GPIO.LOW)
    usleep(2)
    GPIO.output(TP, GPIO.HIGH)
    usleep(10)
    GPIO.output(TP, GPIO.LOW)
    while(GPIO.input(EP) == GPIO.LOW):
        pass
    nStartTime = dt.datetime.now()
    while(GPIO.input(EP) == GPIO.HIGH):
        pass
    nEndTime = dt.datetime.now()
    fDistance = (nEndTime - nStartTime).microseconds/29./2.
    
    return str(fDistance)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TP, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(EP, GPIO.IN)
time.sleep(0.5)
def sendDistance(c):
    while(1):
        # fDistance = getDistance()
        # fD = fDistance.encode()
        fD = "Hello, World!"
        print('send to client,', fD)
        fD = fD.encode()
        c.sendall(fD)
        time.sleep(2)

# Using Multi-Thread
def getTime(c):
    while(1):
        print('Wait for Receiving\n')
        data = c.recv(1030)
        print("Received Start Time to Client", data.decode())
        startTime = datetime.datetime.strptime(data.decode(), "%H:%M:%S").time()
    
        data = c.recv(1030)
        print("Received End Time to Client", data.decode())
        endTime = datetime.datetime.strptime(data.decode(), "%H:%M:%S").time()
        isSound(startTime, endTime)
    
# play music if startTime < now < endTime and SensorData != 0
def isSound(s, e):
    pygame.init()
    now = datetime.datetime.now().time()
    if now > s and now < e:
        print('Music on\n')
        pygame.mixer.Sound('/home/eunnho/python/Pi-socket/alarm.wav').play(-1)
    else:
        print('Music off\n')
        pygame.mixer.stop()
        
# Socket
# HOST = socket.gethostbyname(socket.getfqdn())
HOST = '192.168.0.26'
url = 'https://43.201.130.48:8484/connection'
PORT = 9999

response = requests.post(url, json={'privateIp':HOST}, verify=False)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen()

client_socket, addr = server_socket.accept()

print('Connected by', addr)

tsend = threading.Thread(target = sendDistance, args=(client_socket,), daemon=True)
tgetTime = threading.Thread(target = getTime, args=(client_socket,))
tgetTime.start()
tsend.start()
tgetTime.join()
tsend.join()
    
client_socket.close()
server_socket.close()

