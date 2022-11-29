# Temp 클라이언트 
import socket
import requests
import asyncio
import urllib3
import threading
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

urlAuth = 'https://43.201.130.48:8484/auth/login'
urlRegi = 'https://43.201.130.48:8484/auth/register'
urlip = 'https://43.201.130.48:8484/connection'
PORT = 9999       

# POST /auth/register
responseRegi = requests.post(urlRegi, json={
  'userid' : 'asdasd',
  'password': 'asdasd',
  'nickname': 'asdasd'
}, verify=False)

# POST /auth/login
responseAuth = requests.post(urlAuth, json={
  'userid': 'asdasd',
  'password': 'asdasd'
}, verify=False).json()
accessToken = responseAuth['data']['accessToken']
refreshToken = responseAuth['data']['refreshToken']

# GET/ connection - get internal ip for create connection on android
header = {
  'authorization' : 'Bearer ' + accessToken,
  'refresh': 'Bearer ' + refreshToken
}
response = requests.get(urlip, verify=False, headers=header).json()
print(response)

HOST = response['ip']

def sendTime(c):
  sTime = input("input Start Time")
  c.send(sTime.encode())
  print("Send StartTime Successfully")
  eTime = input("input End Time")
  c.send(eTime.encode())
  print("Send EndTime Successfully")

def getData(c):
  while(1):
    data = c.recv(1030)
    print('Received', repr(data.decode()))

if (HOST):
    # 소켓 객체를 생성합니다. 
    # 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.  
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 지정한 HOST와 PORT를 사용하여 서버에 접속합니다. 
    client_socket.connect((HOST, PORT))

    tget = threading.Thread(target=getData, args=(client_socket,), daemon=True)
    tsend = threading.Thread(target=sendTime, args=(client_socket,))
    tsend.start()
    tget.start()
    tsend.join()
    tget.join()
    # 소켓을 닫습니다.
    client_socket.close()

