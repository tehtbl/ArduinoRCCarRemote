#!/usr/bin/env python

import os
import sys
import termios
import fcntl
import serial
from optparse import OptionParser

parser = OptionParser(usage="usage: %prog [options] arg1 arg2")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="verbose on")
parser.add_option("-d", "--device", dest="device", type="string", help="tty to interact with Arduino")

(opts, args) = parser.parse_args()

def getch():
  fd = sys.stdin.fileno()

  oldterm = termios.tcgetattr(fd)
  newattr = termios.tcgetattr(fd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)

  oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

  try:
    while 1:
      try:
        c = sys.stdin.read(1)
        break
      except IOError: pass
  finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
  return c

if __name__ == "__main__":

    if not opts.device:
        print "no device given..."
        sys.exit(0)

    print "connecting to %s" % (opts.device)
    try:
        ser = serial.Serial(opts.device, 9600)
    except:
        print "not connected :("

    while True:
        print ">>> ",
        ch = (getch()).lower()
        print ch

        if ch == 'x':
            break

        elif ch == '1':
            print "turning on"
            ser.write('1')

        elif ch == '0':
            print "turning off"
            ser.write('0')

        elif ch == 'w':
            print "FWD"
            ser.write('w')

        elif ch == 's':
            print "RWD"
            ser.write('s')

        elif ch == 'a':
            print "LFT"
            ser.write('a')

        elif ch == 'd':
            print "RGT"
            ser.write('d')

        else:
            print "got '%s' -> no idea what to do" % (ch)

    print "bye."

