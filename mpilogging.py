'''
This module is responsible for adding the MPI task id to every logged
message. It uses the standard logging.LoggerAdapter. In order
for it to work, the task, after it initializes MPI, has to call

  mpilogging.log_tid['tid']=rank

and, at the top of each file, instead of creating a logger with
logging.getLogger(__name__), use instead

  logger = mpilogging.mpi_logger(__name__)

Thereafter, all messages will have the tid appended.
'''
import logging


log_tid = { 'tid' : -1 }


def mpi_logger(name):
    add_tid=logging.LoggerAdapter(logging.getLogger(name), log_tid)
    return add_tid
