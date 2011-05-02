import os
import logging
import logging.handlers
import argparse
import numpy
from mpi4py import MPI
import mpilogging


logger = mpilogging.mpi_logger(__name__)


def mpi_init():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    return comm, rank



def exchange(comm,rank):
    # pass explicit MPI datatypes
    if rank == 0:
        data = numpy.arange(1000, dtype='i')
        comm.Send([data, MPI.INT], dest=1, tag=77)
    elif rank == 1:
        data = numpy.empty(1000, dtype='i')
        comm.Recv([data, MPI.INT], source=0, tag=77)
    else:
        data=None

    # automatic MPI datatype discovery
    if rank == 0:
        data = numpy.arange(100, dtype=numpy.float64)
        comm.Send(data, dest=1, tag=13)
    elif rank == 1:
        data = numpy.empty(100, dtype=numpy.float64)
        comm.Recv(data, source=0, tag=13)

    if rank == 1:
        print rank, str(data)




def setup_logging(userlevel, loghost):
    if loghost:
        handler = logging.handlers.DatagramHandler(loghost,5005)
    else:
        handler = logging.StreamHandler()
    handler.setLevel(userlevel)
    formatter=logging.Formatter('%(asctime)s:%(name)s:%(levelname)s'
                                ':%(tid)d:%(message)s')
    handler.setFormatter(formatter)
    logging.root.addHandler(handler)
    logging.root.setLevel(userlevel)

    if loghost:
        # Add a second handler to print the dire messages to stderr.
        screen = logging.StreamHandler()
        screen.setLevel(logging.WARN)
        screen.setFormatter(formatter)
        logging.root.addHandler(screen)
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MPI sample program')
    parser.add_argument('--loghost',
                        help='Where to send logging messages')
    parser.add_argument('--level', default='info',
                        choices=['trace','debug','info','warn','error'],
                        help='Logging level')
    args = parser.parse_args()

    setup_logging(getattr(logging,args.level.upper()), args.loghost)
    logger.info('start %s %s' % (str(args.loghost),str(args.level)))
    
    comm, rank = mpi_init()
    mpilogging.log_tid['tid']=int(rank)
    logger.debug('mpi initialized')
    exchange(comm, rank)

    comm.barrier()
    MPI.Finalize()
    logger.info('finish')
    
