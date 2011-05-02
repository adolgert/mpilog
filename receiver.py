'''
This is a service to listen for messages from processes
using the UDP logging handler, DatagramHandler. This listener is
meant to run on the head node of a parallel job so that it listens
for debugging messages from the MPI client tasks. It batches up the
messages and writes them to disk every so often. Call it in
the batch file with:

  python receiver.py&
  ibrun python my_program.py
  pkill python

so that you kill it when the job is over. It will save events
before it quits.

The start of this code cema from the Python wiki,
wiki.python.org/moin/UdpCommunication.
'''

import os
import sys
import socket
import signal
import threading
import cPickle
import logging
import logging.handlers


# Using an empty UDP_IP, '', for the bind address mean we will accept
# messages from any host. To limit this to localhost, use
# UDP_IP='127.0.0.1'
UDP_IP=''
UDP_PORT=5005

genlog=logging.FileHandler(filename='head.log')
genlog.setLevel(logging.DEBUG)
memhandler = logging.handlers.MemoryHandler(10000,logging.DEBUG,genlog)
formatter=logging.Formatter('%(asctime)s:%(name)s:%(levelname)s'
                            ':%(tid)d:%(message)s')
genlog.setFormatter(formatter)
logger=logging.getLogger()
logger.addHandler(memhandler)
logger.setLevel(logging.DEBUG)


def bind():
    try:
        sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        sock.bind( (UDP_IP, UDP_PORT) )
    except socket.error:
        logger.exception()
    return sock



def store(sock):
    while True:
        data, addr = sock.recvfrom( 8192 ) # buffer size
        try:
            rec = logging.makeLogRecord(cPickle.loads(data[4:]))
            logger.handle(rec)
        except:
            # This means it was a long record which we'll skip.
            logger.warn('Record could not be unpickled.')
            pass


def on_exit(sig, func=None):
    memhandler.flush()
    genlog.close()
    sys.exit()

        


if __name__ == '__main__':
    signal.signal(signal.SIGTERM,on_exit)
    logfile=open('head.log','w+')
    store(bind())
    
