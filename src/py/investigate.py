import os
import time
import sys
import logging

import interrogator



if __name__ == '__main__':

    pgdb              = sys.argv[1]
    pgdblayer         = sys.argv[2]
    pgdblayercols     = sys.argv[3]
    pcomparelayer     = sys.argv[4]
    pcomparelayercols = sys.argv[5]
    pevidenceroom     = sys.argv[6]
    plogdir           = sys.argv[7]
    
    timestr = time.strftime("%Y%m%d-%H%M%S")

    # CSCL_PUB.xyz -> xyz
    gdblayername = pgdblayer.split('.')[-1]
    cscldossier  = os.path.join(pevidenceroom,gdblayername)
    agoldossier  = os.path.join(pevidenceroom
                               ,'{0}-{1}'.format(gdblayername,'suspect'))

    # ..geodatabase-scripts\logs\dev-investigate-historicdistrict-20250403-160745.log
    targetlog = os.path.join(plogdir 
                            ,'investigate-{0}.log'.format(timestr))

    logging.basicConfig(
        level=logging.INFO,                     
        format='%(asctime)s - %(levelname)s - %(message)s', 
        filename=targetlog,                  
        filemode='w'                         
    )

    logging.info('starting investigation of {0}'.format(pgdblayer))
    logging.info('comparing to {0}'.format(pcomparelayer))

    cscllayer = interrogator.csclfeatureclass(pgdb
                                             ,pgdblayer)

    agollayer = interrogator.hostedfeaturelayer(pcomparelayer
                                               ,gdblayername) # instantiates a unique name in memory

    cscllayer.getevidence(pgdblayercols
                         ,cscldossier)

    agollayer.getevidence(pcomparelayercols
                         ,agoldossier)

    if cscllayer.getdossier(cscldossier) == agollayer.getdossier(agoldossier):
        print("ok")
    else:
        only_in_cscl = cscllayer.getdossier(cscldossier) - agollayer.getdossier(agoldossier)
        if only_in_cscl:
            print("only in cscl: {0}".format(only_in_cscl))

        only_in_agol = agollayer.getdossier(agoldossier) - cscllayer.getdossier(cscldossier)
        if only_in_agol:
            print("only in agol {0}".format(only_in_agol))


    logging.info('investigation complete')

    sys.exit(0)
