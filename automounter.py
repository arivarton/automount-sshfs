import sys
import urllib.request
import time
from subprocess import call
from os import listdir

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
    # Where the share should be mounted to
    elif sys.argv[i] == "-m":
        mountTo = sys.argv[i + 1]
    # Where the share will be mounted from
    elif sys.argv[i] == "-M":
        mountFrom = sys.argv[i + 1]
    # Where the share will be mounted from
    elif sys.argv[i] == "-U":
        userName = sys.argv[i + 1]
    # Where the share will be mounted from
    elif sys.argv[i] == "-f":
        fileShare = sys.argv[i + 1]
    i += 1

count = 0
timeAdded = 0

while True:
    try:
        # Check if url that was set is reachable.
        urllib.request.urlopen(url)
        timeAdded = 0
        # If the connection has been false or not checked before. Mount drives.
        if len(listdir(mountTo)) == 0:
            print(str(count) + " - " + time.strftime("%d.%m.%Y - %H:%M:%S: ") + "Opened " + url + " successfully. Mounting drives.")
            call(["sshfs", userName + "@" + fileShare + ":" + mountFrom, mountTo])
        # If the drive is already mounted.
        else:
            print(str(count) + " - " + time.strftime("%d.%m.%Y - %H:%M:%S: ") + "Connection is up but the directory is already mounted.")
        time.sleep(float(timeToSleepSuccesfull * 60))
    # If urlopen fails
    except urllib.error.URLError as err:
        print(str(count) + " - " + time.strftime("%d.%m.%Y - %H:%M:%S: ") + str(err))
        if (count * timeToSleep) >= (int(addTime) * 60):
            time.sleep(float(timeToAdd * 60))
        else:
            time.sleep(float(timeToSleep))
    count += 1
