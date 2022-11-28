# Temp 클라이언트 
import socket
import requests
import asyncio
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

urlAuth = 'https://43.201.130.48:8484/auth/login'
urlRegi = 'https://43.201.130.48:8484/auth/register'
urlip = 'https://43.201.130.48:8484/connection'
PORT = 9999       

# POST /auth/register
responseRegi = requests.post(urlRegi, json={
  'userid' : 'asd',
  'password': 'asd',
  'nickname': 'asd'
}, verify=False)

# POST /auth/login
responseAuth = requests.post(urlAuth, json={
  'userid': 'asd',
  'password': 'asd'
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

if (HOST):
    # 소켓 객체를 생성합니다. 
    # 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.  
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 지정한 HOST와 PORT를 사용하여 서버에 접속합니다. 
    client_socket.connect((HOST, PORT))

    while(1):
    # 메시지를 수신합니다. 
      data = client_socket.recv(1030)
      print('Received', repr(data.decode()))
    # 소켓을 닫습니다.
    client_socket.close()

