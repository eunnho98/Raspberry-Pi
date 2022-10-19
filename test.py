import secrets
import requests
import time
import schedule

def getChannelInfo_second():
  response = requests.get("https://163.180.173.170:8484/channel/device", verify=False)
  print(response.content)

schedule.every(3).seconds.do(getChannelInfo_second)

while True:
  schedule.run_pending()
  time.sleep(1)