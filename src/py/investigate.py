import os
import time
import sys
import logging
import argparse

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

    parser = argparse.ArgumentParser(description="Investigate suspects")

    # Required arguments
    parser.add_argument("gdb", help="Path to the cscl geodatabase")
    parser.add_argument("gdblayer", help="Featureclass name in cscl")
    parser.add_argument("gdblayercols", help="Comma delimited list of cscl columns")
    parser.add_argument("externalsource", help="External layer url or database name")
    parser.add_argument("externallayercols", help="Comma delimited list of external columns")
    parser.add_argument("evidenceroom", help="Directory for evidence storage")
    parser.add_argument("logdir", help="Directory for logs")

    # Optional arguments
    parser.add_argument("--postgistable", help="External postgis table name", default=None)
    parser.add_argument("--gdbwhereclause", help="Where clause for cscl", default=None)
    parser.add_argument("--externalwhereclause", help="Where clause for external", default=None)
    parser.add_argument("--shapecolumn", help="Name of the approximating cscl shape column", default=None)
    parser.add_argument("--externalshapecolumn", help="Name of the approximating external shape column", default=None)
    # these next two may need to be split into cscl vs external if units cause issues
    parser.add_argument("--rounddigits", type=int, help="Number of digits to round shape values", default=1)
    parser.add_argument("--convertfactor", type=float, help="Conversion factor for shape values", default=1.0)

    args = parser.parse_args()

    # CSCL_PUB.xyz -> xyz is better for naming log and evidence files
    cscllayername     = args.gdblayer.split('.')[-1]

    setuplogger('investigate'
               ,cscllayername
               ,args.logdir)
    logger = logging.getLogger('investigate')

    logger.info('starting investigation of {0}'.format(args.gdblayer))
    logger.info('comparing to {0}'.format(args.externalsource))

    # \evidencelocker1\borough
    # \evidencelocker1\borough-suspect
    cscldossier      = os.path.join(args.evidenceroom
                                   ,cscllayername)
    externaldossier  = os.path.join(args.evidenceroom
                                   ,'{0}-{1}'.format(cscllayername,'suspect'))

    cscllayer = interrogator.csclfeatureclass(args.gdb
                                             ,args.gdblayer)

    if args.externalsource.lower().startswith('http'):
        externallayer = interrogator.hostedfeaturelayer(args.externalsource
                                                       ,args.gdblayer) # this is a meaningless arcpy in-memory tag
    else:
        externallayer = interrogator.postgistable(args.externalsource
                                                 ,args.postgistable)

    cscllayer.getevidence(args.gdblayercols
                         ,cscldossier
                         ,args.shapecolumn
                         ,args.rounddigits
                         ,args.convertfactor
                         ,args.gdbwhereclause)

    externallayer.getevidence(args.externallayercols
                             ,externaldossier
                             ,args.externalshapecolumn
                             ,args.rounddigits
                             ,args.convertfactor
                             ,args.externalwhereclause)

    if cscllayer.getdossier(cscldossier) == externallayer.getdossier(externaldossier):
        logger.info('Complete exoneration of suspect {0}'.format(args.externalsource))
    else:   
        reportproof(cscllayer.getdossier(cscldossier)
                   ,externallayer.getdossier(externaldossier))     
        
    logger.info('investigation complete')

    sys.exit(0)

if __name__ == '__main__':
    main()