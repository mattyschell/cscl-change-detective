import arcpy

class csclfeatureclass(object):

    def __init__(self
                ,gdb
                ,layer):

        # file geodatabase or enterprise geodatabase
        self.gdb   = gdb
        self.layer = layer

    def getevidence(self
                   ,columns 
                   ,dossierfile):

        arcpy.env.workspace = self.gdb

        columnlist = [f.strip() for f in columns.split(",")]

        with open(dossierfile, 'w') as f: 
            with arcpy.da.SearchCursor(self.layer
                                      ,columnlist) as cursor:
                for row in cursor:
                    f.write(",".join(str(item) for item in row) + "\n")

        arcpy.env.workspace = None

    def getdossier(self
                  ,dossierfile):
        
        # this class is agnostic about the dossier location
        # we may interrogate multiple times 
        # producing multiple dossiers

        with open(dossierfile,'r') as f:
            unordereddossier = {line.strip() for line in f}

        # return type is a set containing text
        # permits comparison without regard to order
        # dont be scared python uses hash based lookups
        # several million elements are totally fine
        return unordereddossier

class hostedfeaturelayer(object):

    def __init__(self):
        pass

class postgistable(object):

    def __init__(self):
        pass
