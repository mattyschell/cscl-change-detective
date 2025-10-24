import os
import time
import sys
import logging

import interrogator


def reportproof(gdblayerset
               ,externallayerset):
    
    logger = logging.getLogger('investigate')
    
    gdbonly = gdblayerset - externallayerset
    if gdbonly:
        logger.warning('These values are only in the geodatabase')
        for evidence in gdbonly:
            logger.warning(evidence)

    externalonly = externallayerset - gdblayerset
    if externalonly:
        logger.warning('These values are only in the external dataset')
        for evidence in externalonly:
            logger.warning(evidence)

def setuplogger(loggername
               ,layername
               ,logdirectory):

    # ..geodatabase-scripts\logs\dev-investigate-historicdistrict-20250403-160745.log
    targetlog = os.path.join(logdirectory 
                            ,'investigate-{0}-{1}.log'.format(layername
                                                             ,time.strftime("%Y%m%d-%H%M%S")))

    logger = logging.getLogger(loggername)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(targetlog, mode='w')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

def main():

    pgdb               = sys.argv[1]
    pgdblayer          = sys.argv[2]
    pgdblayercols      = sys.argv[3]
    pexternallayer     = sys.argv[4]
    pexternallayercols = sys.argv[5]
    pevidenceroom      = sys.argv[6]
    plogdir            = sys.argv[7]
    
    # CSCL_PUB.xyz -> xyz
    gdblayername     = pgdblayer.split('.')[-1]

    setuplogger('investigate'
               ,gdblayername
               ,plogdir)
    logger = logging.getLogger('investigate')

    logger.info('starting investigation of {0}'.format(pgdblayer))
    logger.info('comparing to {0}'.format(pexternallayer))

    cscldossier      = os.path.join(pevidenceroom,gdblayername)
    externaldossier  = os.path.join(pevidenceroom
                                   ,'{0}-{1}'.format(gdblayername,'suspect'))

    cscllayer = interrogator.csclfeatureclass(pgdb
                                             ,pgdblayer)

    externallayer = interrogator.hostedfeaturelayer(pexternallayer
                                                   ,gdblayername) # instantiates a unique name in memory

    cscllayer.getevidence(pgdblayercols
                         ,cscldossier)

    externallayer.getevidence(pexternallayercols
                             ,externaldossier)

    if cscllayer.getdossier(cscldossier) == externallayer.getdossier(externaldossier):
        logger.info('Full exoneration of {0}'.format(pexternallayer))
    else:   
        reportproof(cscllayer.getdossier(cscldossier)
                   ,externallayer.getdossier(externaldossier))     
        
    logger.info('investigation complete')

    sys.exit(0)

if __name__ == '__main__':
    main()