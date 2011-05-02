import os
import logging
import logging.handlers
import signal
import time

logger=logging.getLogger(__name__)

def setup_logging(userlevel):
    userlevel=logging.DEBUG
    handler = logging.handlers.DatagramHandler('localhost',5005)
    handler.setLevel(userlevel)
    formatter=logging.Formatter('%(asctime)s:%(name)s:%(levelname)s'
                                '%(message)s):'+str(os.getenv('HOST')))
    logging.root.addHandler(handler)
    logging.root.setLevel(userlevel)

def on_exit(sig, func=None):
    print 'exiting'

signal.signal(signal.SIGTERM,on_exit)


setup_logging(logging.DEBUG)
logger.debug('hiya')
