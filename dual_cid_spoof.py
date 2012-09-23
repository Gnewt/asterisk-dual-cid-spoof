#!/usr/bin/env python

# Author: Gnewt <http://www.gnewt.at>
# Date: 07/01/12
# Title: Asterisk Dual CID Spoof
# License: WTFPL <http://sam.zoy.org/wtfpl/>

from os import rename
from time import sleep
import sys

# --------------- change the following ---------------
# Change this to the number of your conference room,
# defined in meetme.conf.
CONFNUM = 1234
# Change this to your outgoing SIP trunk's name.
SIPTRUNK = "flowroute"
# --------------- end user changes -------------------

def write(stuff):
    """Writes something to the AGI interface (and to stderr)."""
    sys.stdout.write("%s\n" % stuff)
    sys.stdout.flush()
    sys.stderr.write("%s\n" % stuff)
    sys.stderr.flush()
def stream(file):
    """Streams a builtin Asterisk sound file."""
    write("STREAM FILE %s \"\"" % file)

def make_call_files(num1, num2):
    """Makes the two call files in /tmp, then moves to asterisk's spool directory."""
    callfile_buffer = """Channel: SIP/{0}/1{1}
CallerID: "" <{2}>
Application: MeetMe
Data: {3},xq
"""
    file1 = open("/tmp/dualcall-1.call","w")
    file2 = open("/tmp/dualcall-2.call","w")
    file1.write(callfile_buffer.format(SIPTRUNK, num1, num2, CONFNUM))
    file2.write(callfile_buffer.format(SIPTRUNK, num2, num1, CONFNUM))
    file1.close()
    file2.close()
    rename("/tmp/dualcall-1.call", "/var/spool/asterisk/outgoing/dualcall-1.call")
    rename("/tmp/dualcall-2.call", "/var/spool/asterisk/outgoing/dualcall-2.call")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        make_call_files(sys.argv[1], sys.argv[2])
        stream("agent-loginok")
        sleep(2)
        write("EXEC MeetMe \"{0},samqA\"".format(CONFNUM))
        write("HANGUP")

