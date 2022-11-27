import socket
import requests
import asyncio

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

# Socket
HOST = '192.168.0.26'
url = 'http://192.168.0.7:3000/api/ip'
PORT = 9999

response = requests.post(url, json={'myIP':HOST})
print(response.content)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen()

client_socket, addr = server_socket.accept()

print('Connected by', addr)

while True:
    #data = client_socket.recv(1030)
    fDistance = getDistance()
    fD = fDistance.encode()
    #if not data:
    #    break
    #print('Received from', addr, data.decode())
    #client_socket.sendall(data)
    client_socket.sendall(fD)
    time.sleep(1)
    
client_socket.close()
server_socket.close()
