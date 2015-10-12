"""
    Simple program that mimics speedtest.net and returns MBPS for 
    network.
    To make it more interesting,I added a threading aspect
    to run the wget command in a background thread and signal
    an event once it is finished.
    Author: Darshan Thaker
"""
import sys
import os
import math
import time
import threading
import subprocess

globtime = 0 

class Command(object):
    """
        Command class that takes in an event and a command to run.
        The class will start a daemon (background) thread running the 
        command.
    """
    def __init__(self, cmd, thread_ready):
        self.cmd = cmd
        self.process = None
        self.thread_ready = thread_ready
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    """
        At the end of the run, when the command has finished, signal the
        thread_ready event, which signals that the given command has finished.
        The time is kept track through a global time variable. 
    """
    def run(self):
        global globtime
        globtime = time.clock()
        self.process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        (out, err) = self.process.communicate()
        self.thread_ready.set()
    
        
"""
    Experiment with threading to calculate MBPS for a network.
    Flaws in the code:
        1. Time does not take into account overhead for context switching
        2. Sample 5MB file is downloaded from server in U.K. (found out through
        traceroute). This means the MBPS also takes into account time it takes
        to transport the file from that server to the local ISP.
"""
def main():
    FILE_SIZE = 5
    thread_ready = threading.Event()
    # Download a test 5MB file.
    command = Command("wget http://download.thinkbroadband.com/5MB.zip", thread_ready)
    while not thread_ready.isSet():
        try:
            time.sleep(0)
        except KeyboardInterrupt:
            print "CONTROL C RECEIVED: SENDING KILL SIGNAL"
            thread_ready.set()
            process = subprocess.Popen("rm 5MB.zip", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            (out, err) = process.communicate()
            sys.exit()
    print "DONE WITH WGET"
    timetaken = time.clock() - globtime
    print "Total took: " + str(timetaken) + " seconds"
    print "MBPS: " + str((FILE_SIZE*8)/timetaken)
    process = subprocess.Popen("rm 5MB.zip", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    (out, err) = process.communicate()

if __name__=='__main__':
    main()
