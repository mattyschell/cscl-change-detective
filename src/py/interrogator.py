import arcpy

class csclitem(object):

    def __init__(self
                ,gdb
                ,layer):

        self.gdb   = gdb
        self.layer = layer

    def getevidence(self
                   ,columns 
                   ,dossier):

        arcpy.env.workspace = self.gdb

        columnlist = [f.strip() for f in columns.split(",")]

        with open(dossier, 'w') as f: 
            with arcpy.da.SearchCursor(self.layer
                                      ,columnlist) as cursor:
                for row in cursor:
                    f.write(",".join(str(item) for item in row) + "\n")

        self.dossier = dossier

    def getdossier(self):

        with open(self.dossier,'r') as f:
            unordereddossier = {line.strip() for line in f}

        return unordereddossier