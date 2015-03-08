import logging
import splunk.Intersplunk as si
import os
import subprocess
from splunk.appserver.mrsparkle.lib.util import make_splunkhome_path

USER = 'ubuntu'
SSH_KEY = make_splunkhome_path(['etc', 'apps', 'bsides-austin-2015-app','default','bsides_demo.pem'])

def setup_logger():
    """
    sets up logger for shutdown command
    """
    logger = logging.getLogger('bsides')
    # Prevent the log messgaes from being duplicated in the python.log
    #    AuthorizationFailed
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    file_handler = logging.handlers.RotatingFileHandler(
                    make_splunkhome_path(['etc', 'apps', 'bsides-austin-2015-app', 'logs',
                                          'bsides.log']),
                                        maxBytes=25000000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
logger = setup_logger()


def prockill(pid,process_name,endpoint):
    
    if pid:
        ssh = subprocess.Popen(['ssh', '-o StrictHostKeyChecking=no', '-i{0}'.format(SSH_KEY), '{0}@{1}'.format(USER,endpoint), 'sudo kill -9', pid], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        if result == []:
            error = ssh.stderr.readlines()
            logger.error(error)
        else:
            logger.debug(result)
    
    if process_name:
        ssh = subprocess.Popen(['ssh', '-o StrictHostKeyChecking=no', '-i{0}'.format(SSH_KEY), '{0}@{1}'.format(USER,endpoint), 'sudo killall', process_name], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        if result == []:
            error = ssh.stderr.readlines()
            logger.error(error)
        else:
            logger.debug(result)

if __name__ == '__main__':

    try:
        results, dummyresults, settings = si.getOrganizedResults()
        keywords, options = si.getKeywordsAndOptions()
         
        for entry in results:
            ## parse arguments
            if "endpoint" in entry:
                endpoint = entry["endpoint"]
            else:
                endpoint = options.get('endpoint', None)

            if "pid" in entry:
                pid = entry["pid"]
            else:
                pid = options.get('pid', None)

            if "process_name" in entry:
                process_name = entry["process_name"]
            else:
                process_name = options.get('process_name', None)

            #kill process
            prockill(pid,process_name,endpoint)
            logger.warn('sent process kill command for PID {0} name {1} to host {2})'.format(pid,process_name,endpoint))
            break

    except Exception as e:
        logger.error("There was an issue establishing arguments for the " +
                     "prockill search command!")
        logger.exception(str(e))

