import arcpy

class csclitem(object):

    def __init__(self
                ,gdb
                ,layer):

        # file geodatabase or enterprise geodatabase
        self.gdb         = gdb
        self.layer       = layer

        # this is a global env
        # not sure how i feel about using it
        arcpy.env.workspace = self.gdb
        self.desc = arcpy.Describe(self.layer)

        # always include area, length, or xy



        arcpy.env.workspace = None

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
        # we may interrogate multiple times for multiple dossiers

        with open(dossierfile,'r') as f:
            unordereddossier = {line.strip() for line in f}

        # return type is set so we can compare without regard to order
        return unordereddossier