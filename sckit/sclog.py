import logging
import time
import numpy as np

def sclog_time_start(process_name):
    '''
    time start
    '''
    return (time.time(), process_name)

def sclog_time_split(logger, start_time):
    '''
    time end / split
    '''
    logger.info('TIME EVAL SPLIT [{}]: {} secs.'.format(start_time[1], np.round(time.time() - start_time[0],6)))

def sclog_basicConfig(log_level, log_filename='', log_filemode='a'):
    '''    
    input:
        log_level: Such as logging.WARN.
        log_filename: Filename of the log file. It can be left as empty if you
        wanna just print out the log info.
    '''
    logging.basicConfig(level=log_level,
                        filename=log_filename,
                        filemode=log_filemode,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s %(levelname)-8s [%(filename)s:%(name)s()], line %(lineno)d, \"%(message)s\"')

if __name__ == '__main__':
    
    sclog_basicConfig(logging.INFO)

    time_start = sclog_time_start('main()')
    logger = logging.getLogger('main')

    logger.debug('debug msg')
    logger.info('info msg')
    logger.warn('warn msg')
    logger.error('error msg')
    logger.critical('critical msg')

    sclog_time_split(logger, time_start)
