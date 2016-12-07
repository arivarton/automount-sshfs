import sys
import time
import logging
import argparse
from subprocess import call
from os import listdir

# Setup log file
FORMAT = logging.basicConfig(filename=".automount-sshfs.log", 
        filemode='a',
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.DEBUG, 
        datefmt='%H:%M:%S')
logger = logging.getLogger('automounter')

def main():
    parser = argparse.ArgumentParser(description='''Mounts folders with ssh. Continues monitoring
            for connection and mounts again if connection is lost.''',
            epilog='By arivarton (http://www.arivarton.com)')
    parser.add_argument('-t', '--initial_sleep', type=str, help='''Time to sleep before attempting
            to connect again after failure.''', default=1)
    parser.add_argument('-s', '--succesfull_sleep', type=str, help='''Time to sleep before
            checking that the mount is still present.''', default=2)
    parser.add_argument('-a', '--wait_sleep_addition', type=str, help='''Minutes to wait until
            sleep timer gets set higher.''', default=5)
    parser.add_argument('-T', '--add_sleep', type=str, help='Add time to sleep timer.', default=2)
    parser.add_argument('-m', '--mount_directory', type=str, help='Mount location.')
    parser.add_argument('-M', '--file_directory', type=str, help='''Location of the folder to
            mount.''') 
    parser.add_argument('-U', '--username', type=str, help='Username.')
    parser.add_argument('-f', '--fileshare', type=str, help='Fileshare to mount from.')
    args = parser.parse_args()
    mount(args)

def mount(args):
    logging.info("Mounting from: " + str(args.mount_directory) + "\nto: " + str(args.file_directory))
    count = 0
    while True:
        sleep = sleepCounter(count)
        # If the connection has been false or not checked before. Mount drives.
        if len(listdir(args.mount_directory)) == 0:
            if call(['ping', args.fileshare, '-q', '-c', '1']):
                logging.info("Failed to contact " + args.fileshare + " trying again in " + args.succesfull_sleep + " minutes.")
            else:
                logging.info("Contacted " + args.fileshare + " successfully. Mounting drives.")
                callString = "sshfs", args.username + "@" + args.fileshare + ":" + args.file_directory, args.mount_directory
                call(callString)
                logging.debug(str(callString))
                count = 0
        # If the drive is already mounted.
        else:
            logging.info('''Connection is up but the directory is already mounted, trying again
                    in ''' + sleep / 60 + ' minutes.')
        time.sleep(sleep)
        count += 1

# If the script has run longer than wait_sleep_addition variable is set to
# increase the sleep variable
def sleepCounter(count):
    if (count * (args.initial_sleep * 60)) >= (int(args.wait_sleep_addition) * 60):
        return float((args.initial_sleep * 60) + (args.add_sleep * 60))
    else:
        return float(args.initial_sleep * 60)


if __name__ == '__main__':
    main()
