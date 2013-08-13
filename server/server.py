#!/usr/bin/env python

#
# TODO
#
#   queue serial sendings,
#   if '2' happens put it in the first queue slot...
#

import os
import sys
import termios
import fcntl
import serial

import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs

import pprint
pp = pprint.PrettyPrinter(indent=2)

from optparse import OptionParser

parser = OptionParser(usage="usage: %prog [options] arg1 arg2")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="verbose on")
parser.add_option("-d", "--device", dest="device", type="string", help="tty to interact with Arduino")

parser.add_option("-i", "--interactive", action="store_true", dest="interactive", default=False, help="use interactive mode")
parser.add_option("-w", "--webserver", action="store_true", dest="webserver", default=False, help="use webserver mdoe")

(opts, args) = parser.parse_args()


# handler from web requests
class MyHandler(BaseHTTPRequestHandler):

#    def __init__(self, ser, *args, **kw):
#        self.ser = ser
#        BaseHTTPRequestHandler.__init__(self, *args, **kw)


    def do_GET(self):
        try:
            # TODO: no security checks!!!

            nn = []
            params = {}
            new_path = ""

            if "?" in self.path:
                nn = self.path.split('?')
                new_path = nn[0]
                params = parse_qs(urlparse("?"+nn[1]).query)
                #doSend(params['send'][0], self.ser)
                #doSend(params['send'][0], ser)
                doSend(params['send'][0])
            else:
                new_path = self.path

            if new_path == "/" or new_path == "":
                new_path = "/index.html"

            print "path:", new_path
            print "params:", pp.pprint(params)
            f = open(curdir + sep + new_path)
            self.send_response(200)

            if new_path.endswith(".html"):
                self.send_header('Content-type', 'text/html')
            elif new_path.endswith(".js"):
                self.send_header('Content-type', 'text/javascript')
            elif new_path.endswith(".css"):
                self.send_header('Content-type', 'text/css')
            else:
                self.send_header('Content-type', 'text/plain')

            self.end_headers()
            self.wfile.write(f.read())
            f.close()

            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)


# get char from stdin
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



# send the commands to serial dev
#def doSend(ch, ser):
def doSend(ch):
    if ch == '1':
        print "turning on"
        ser.write('1')

    elif ch == '0':
        print "turning off"
        ser.write('0')

    elif ch == '2':
        print "stopping"
        ser.write('2')

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

    elif ch == '4':
        print "FWD LFT"
        ser.write('4')

    elif ch == '5':
        print "FWD RGT"
        ser.write('5')

    elif ch == '8':
        print "RWD LFT"
        ser.write('8')

    elif ch == '9':
        print "RWD RGT"
        ser.write('9')

    else:
        print "got '%s' -> no idea what to do" % (ch)


#
# MAiN
#
if __name__ == "__main__":

    # connect device
    if not opts.device:
        print "no device given..."
        sys.exit(0)

    print "connecting to %s" % (opts.device)
    try:
        ser = serial.Serial(opts.device, 9600)
    except:
        print "not connected :("

    # check the mode to use
    if (not opts.interactive and not opts.webserver) or (opts.interactive and opts.webserver):
        print "use either -i or -w"
        sys.exit(0)

    # interactive mode
    if opts.interactive:
        while True:
            print ">>> ",
            ch = (getch()).lower()
            print ch
            if ch == 'x':
                break
            else:
                #doSend(ch, ser)
                doSend(ch)

    # webserver mode
    elif opts.webserver:

        #def handler(*args):
        #    MyHandler(ser, *args)

        try:
            #server = HTTPServer(('0.0.0.0', 4280), handler)
            server = HTTPServer(('', 4280), MyHandler)
            print 'started httpserver...'
            server.serve_forever()
        except KeyboardInterrupt:
            print '^C received, shutting down server'
            server.socket.close()

    print "bye."
