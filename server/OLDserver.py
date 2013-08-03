#!/usr/bin/env python

import readline
import logging
import sys
import serial
import select
from optparse import OptionParser

parser = OptionParser(usage="usage: %prog [options] arg1 arg2")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="verbose on")
parser.add_option("-i", "--interactive", action="store_true", dest="interactive", default=False, help="interactive mode on")
parser.add_option("-d", "--device", dest="device", type="string", help="tty to interact with Arduino")
parser.add_option("-p", "--port", dest="port", default=8585, type="int", help="port number to run on")
parser.add_option("-c", "--command", dest="cmd", type="string", help="string to send")

LOG_FILENAME = '/tmp/completer.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

CMDS = ['quit', 'send', 'connect', 'exit']

class SimpleCompleter(object):

    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
        # This is the first time for this text, so build a match list.
            if text:
                self.matches = [s
                                for s in self.options
                                if s and s.startswith(text)]
                logging.debug('%s matches: %s', repr(text), self.matches)
            else:
                self.matches = self.options[:]
                logging.debug('(empty input) matches: %s', self.matches)

        # Return the state'th item from the match list,
        # if we have that many.
        try:
            response = self.matches[state]
        except IndexError:
            response = None
            logging.debug('complete(%s, %s) => %s',
            repr(text), state, repr(response))

        return response

def input_loop():
    line = ''
    if opts.device != None:
        try:
            ser = serial.Serial(opts.device, 9600)
            prefix = '[%s] ' % (opts.device)
        except:
            prefix = 'error connecting to %s ' % (opts.device)
    else:
        prefix = ''

    while line != 'quit':
        line = raw_input('%s>>> ' % (prefix) )
        #print 'Dispatch %s' % line

        cmd, arg = line.split(' ')
        if not cmd in CMDS:
            pass

        print "sending command: '%s'" % (line)
        ser.write(line)

        if line.startswith("send"):
            print "sending '%s'" % (arg)


(opts, args) = parser.parse_args()

if __name__ == "__main__":

    if opts.interactive:
        # Register our completer function
        readline.set_completer(SimpleCompleter(CMDS).complete)

        # Use the tab key for completion
        readline.parse_and_bind('tab: complete')

        # Prompt the user for text
        input_loop()

        sys.exit(0)

    if opts.device == None:
        print "no device given: try help"
        sys.exit(1)

    if opts.cmd == None:
        print "no command given: try help"
        sys.exit(1)


    print "trying to connect to arduino via %s" % (opts.device)

#    try:
    ser = serial.Serial(opts.device, 9600)
    print "sending command: '%s'" % (opts.cmd)
    ser.write(opts.cmd)
#    while True:
#    print ser.readline().strip()
#    except:
#        pass





