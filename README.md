This is a simple program that mimics the functionality of speedtest.net and returns the MBPS (megabits per second) for a network connection. It runs wget on a 5MB download file and times the download to calculate MBPS.

 To make it more interesting, I added a threading aspect to run the wget command in a background thread and signal an event once it is finished. 

There are two threads running: the main thread, which handles the printing out of status and the background thread which is executing the wget command through a subprocess to the shell.
