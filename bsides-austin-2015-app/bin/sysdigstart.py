import logging
import splunk.Intersplunk as si
import os
import subprocess
from splunk.appserver.mrsparkle.lib.util import make_splunkhome_path

USER = 'ubuntu'
SSH_KEY = make_splunkhome_path(['etc', 'apps', 'bsides-austin-2015-app','default','bsides_demo.pem'])

#makes a local path to store logs to be ingested in inouts.conf
BASE_DIR = make_splunkhome_path(["etc","apps","TA-Akamai"])

#adjusted for windows path
EVIDENCE_LOG_PATH = os.path.join(BASE_DIR,'log','evidence.log')


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


def sysdigstart(process_name,endpoint):
    
    if process_name:
        ssh = subprocess.Popen(['ssh', '-o StrictHostKeyChecking=no', '-i{0}'.format(SSH_KEY), '{0}@{1}'.format(USER,endpoint), 'sysdig -v proc.name contains', process_name], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        if result == []:
            error = ssh.stderr.readlines()
            logger.error(error)
        else:
            logger.debug(result)
            return result

if __name__ == '__main__':

    try:
        results, dummyresults, settings = si.getOrganizedResults()
        keywords, options = si.getKeywordsAndOptions()
        #opens a file handle to write results into
        bufsize = 0
        f = open(EVIDENCE_LOG_PATH, 'w',bufsize)
         
        for entry in results:
            ## parse arguments
            if "endpoint" in entry:
                endpoint = entry["endpoint"]
            else:
                endpoint = options.get('endpoint', None)

            if "process_name" in entry:
                process_name = entry["process_name"]
            else:
                process_name = options.get('process_name', None)

            #kill process
            result = prockill(process_name,endpoint)
            logger.warn('sent sysdig collection to endpoint {0} with a process name that contains {1} )'.format(endpoint,process_name))
            #write results
            f.write(result)


            #should not get here should use the stop command
            break
        f.close()

    except Exception as e:
        logger.error("There was an issue establishing arguments for the " +
                     "sysdig search command!")
        logger.exception(str(e))

