import sys
import urllib.request
import time
import logging
from subprocess import call
from os import listdir

logging.basicConfig(filename=".automount-sshfs.log",level=logging.DEBUG)

# Default values for arguments
url = "http://www.arivarton.com"
timeToSleep = 10
timeToSleepSuccesfull = 2
addTime = 5
timeToAdd = 1

for counter, argument in enumerate(sys.argv):
  # if url is set
    if argument == "-u":
        url = sys.argv[counter + 1]
    # if timeToSleep is set
    elif argument == "-t":
        timeToSleep = sys.argv[counter + 1]
    # Time to sleep after succesfull connection
    elif argument == "-s":
        timeToSleepSuccesfull = sys.argv[counter + 1]
    # Minutes to wait until sleep timer gets set higher
    elif argument == "-a":
        addTime = sys.argv[counter + 1]
    # *Minutes* to sleep after the addition has been set
    elif argument == "-T":
        timeToAdd = sys.argv[counter + 1]
    # Where the share should be mounted to
    elif argument == "-m":
        mountTo = sys.argv[counter + 1]
    # Where the share will be mounted from
    elif argument == "-M":
        mountFrom = sys.argv[counter + 1]
    # Where the share will be mounted from
    elif argument == "-U":
        userName = sys.argv[counter + 1]
    # Where the share will be mounted from
    elif argument == "-f":
        fileShare = sys.argv[counter + 1]

count = 0

while True:
    try:
        # Check if url that was set is reachable.
        urllib.request.urlopen(url)
        # If the connection has been false or not checked before. Mount drives.
        if len(listdir(mountTo)) == 0:
            infoString = str(count) + " - " + time.strftime("%d.%m.%Y - %H:%M:%S: ") + "Opened " + url + " successfully. Mounting drives."
            print(infoString)
            logging.info(infoString)
            call(["sshfs", userName + "@" + fileShare + ":" + mountFrom, mountTo])
            infoString = "sshfs " + userName + "@" + fileShare + ":" + mountFrom + " " + mountTo
            print(str(count) + " - " + time.strftime("%d.%m.%Y - %H:%M:%S: ") + infoString)
            logging.debug(str(count) + " - " + time.strftime("%d.%m.%Y - %H:%M:%S: ") + infoString)
        # If the drive is already mounted.
        else:
            infoString = str(count) + " - " + time.strftime("%d.%m.%Y - %H:%M:%S: ") + "Connection is up but the directory is already mounted."
            print(infoString)
            logging.info(infoString)
        time.sleep(float(timeToSleepSuccesfull * 60))
    # If urlopen fails
    except urllib.error.URLError as err:
        errorString = str(count) + " - " + time.strftime("%d.%m.%Y - %H:%M:%S: ") + str(err)
        print(errorString)
        logging.error(errorString)
        if (count * timeToSleep) >= (int(addTime) * 60):
            time.sleep(float(timeToAdd * 60))
        else:
            time.sleep(float(timeToSleep))
    count += 1
