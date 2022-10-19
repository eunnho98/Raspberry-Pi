import requests
import time

def getChannelInfo_second():
  global data
  response = requests.get("https://naver.com", verify=False)
  data = list(response.headers.keys())

while True:
  getChannelInfo_second()
  if 'Content-Type' in data:
    break
  print(data)
  time.sleep(2)
  