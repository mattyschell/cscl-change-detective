import arcpy

class csclfeatureclass(object):

    def __init__(self
                ,gdb
                ,layer):

        # file geodatabase or enterprise geodatabase
        self.gdb   = gdb
        self.layer = layer

    def roundrow(self
                ,row
                ,rowindex
                ,rounddigits):

        # fish out the rounding column position and round if its a number

        if isinstance(row[rowindex], (float, int)):    
                        
            if rounddigits > 0:
                row[rowindex] = round(row[rowindex], rounddigits)
            else:
                # rounding floats produces floats like 
                # round(123.123,-1) = 120.0 
                # so int() to produce the more expected 120
                row[rowindex] = int(round(row[rowindex], rounddigits))
        
        elif isinstance(row[rowindex], (tuple)): 

            # for points we will often request (x,y) instead of area/length
            # arcpy search cursor returns these as tuples

            if rounddigits > 0:
                row[rowindex] = tuple(round(num, rounddigits) for num in row[rowindex])
            else:
                row[rowindex] = tuple(int(round(num, rounddigits)) for num in row[rowindex])

        return row

    def getevidence(self
                   ,columns 
                   ,dossierfile 
                   ,roundcolumn=None
                   ,rounddigits=1):

        arcpy.env.workspace = self.gdb

        columnlist = [f.strip() for f in columns.split(",")]

        # we support rounding one column only (for now (forever?))
        try:
            round_index = columnlist.index(roundcolumn)
        except ValueError:
            round_index = None
        
        with open(dossierfile, 'w') as f: 
            with arcpy.da.SearchCursor(self.layer
                                      ,columnlist) as cursor:
                for row in cursor:

                    # convert tuple to list
                    row = list(row)
                    
                    if round_index is not None:
                        row = self.roundrow(row
                                           ,round_index
                                           ,rounddigits)

                    # write the evidence to the dossier
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
        # several million elements are fine
        return unordereddossier

class hostedfeaturelayer(object):

    def __init__(self):
        pass

class postgistable(object):

    def __init__(self):
        pass
