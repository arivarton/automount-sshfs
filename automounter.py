import sys
import urllib.request
import time
from subprocess import call

# Default values for arguments
url = "http://www.arivarton.com"
timeToSleep = 10
timeToSleepSuccesfull = 2
addTime = 5
timeToAdd = 1

for i in range(len(sys.argv)):
  # if url is set
  if sys.argv[i] == "-u":
    url = sys.argv[i + 1]
  # if timeToSleep is set
  elif sys.argv[i] == "-t":
    timeToSleep = sys.argv[i + 1]
  # Time to sleep after succesfull connection
  elif sys.argv[i] == "-s":
    timeToSleepSuccesfull = sys.argv[i + 1]
  # Minutes to wait until sleep timer gets set higher
  elif sys.argv[i] == "-a":
    addTime = sys.argv[i + 1]
  # *Minutes* to sleep after the addition has been set
  elif sys.argv[i] == "-T":
    timeToAdd = sys.argv[i + 1]
  i += 1

count = 0
timeAdded = 0
checkConnection = False

while True:
  try:
    # Check if url that was set is reachable.
    urllib.request.urlopen(url)
    # If the connection has been false or not checked before. Mount drives.
    if checkConnection == False:
      print(str(count) + " - " + time.strftime("%d.%m.%Y - %H:%M:%S: ") + "Opened " + url + " successfully. Mounting drives")
      call(["sshfs", "arivarto@arivarton.com:/home/arivarto/public_html/", "/home/arivarton/Development/UMG/"])
    # If the drive is already mounted.
    else:
      print(str(count) + " - " + time.strftime("%d.%m.%Y - %H:%M:%S: ") + "Opened " + url + " successfully again. Did not retry to mount.")
    checkConnection = True
    time.sleep(float(timeToSleepSuccesfull * 60))
  # If urlopen fails
  except urllib.error.URLError as err:
    print(str(count) + " - " + time.strftime("%d.%m.%Y - %H:%M:%S: ") + str(err))
    time.sleep(float(timeToSleep))
    if (((count * timeToSleep) >= (addTime * 60)) & (timeAdded != 1)):
      timeToSleep = timeToAdd * 60
      timeAdded = 1
    checkConnection = False
  except:
    print("Unexpected error:\n\n", sys.exc_info()[0])
    break
  count += 1
