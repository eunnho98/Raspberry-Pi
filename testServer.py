import requests

HOST = '127.0.0.1'

urlip = 'http://localhost:3000/api/ip'

# 클라이언트 접속을 대기하는 포트 번호입니다.   
PORT = 9999   

response = requests.post(urlip, json={'myIP':HOST})
print(response.content)