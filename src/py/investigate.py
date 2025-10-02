import os
import time
import sys
import logging

import interrogator


def reportproof(gdblayerset
               ,externallayerset):
    
    gdbonly = gdblayerset - externallayerset
    if gdbonly:
        logging.warning('These values are only in the geodatabase')
        for evidence in gdbonly:
            logging.warning(evidence)

    externalonly = externallayerset - gdblayerset
    if externalonly:
        logging.warning('These values are only in the external dataset')
        for evidence in externalonly:
            logging.warning(evidence)

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

    timestr = time.strftime("%Y%m%d-%H%M%S")
    # ..geodatabase-scripts\logs\dev-investigate-historicdistrict-20250403-160745.log
    targetlog = os.path.join(plogdir 
                            ,'investigate-{0}-{1}.log'.format(gdblayername
                                                             ,timestr))

    logging.basicConfig(
        level=logging.INFO,                     
        format='%(asctime)s - %(levelname)s - %(message)s', 
        filename=targetlog,                  
        filemode='w')

    logging.info('starting investigation of {0}'.format(pgdblayer))
    logging.info('comparing to {0}'.format(pexternallayer))


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
        logging.info('Full exoneration of {0}'.format(pexternallayer))
    else:   
        reportproof(cscllayer.getdossier(cscldossier)
                   ,externallayer.getdossier(externaldossier))     
        
    logging.info('investigation complete')

    sys.exit(0)

if __name__ == '__main__':
    main()