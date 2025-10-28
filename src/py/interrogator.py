import arcpy
import os
import subprocess
import re
import traceback

class suspects:

    def getevidence(self
                   ,columns 
                   ,dossierfile 
                   ,shapecolumn=None
                   ,rounddigits=1
                   ,convertfactor=1
                   ,whereclause=None):

        raise NotImplementedError("Subclasses implement this method")

    def getdossier(self
                  ,dossierfile):
        
        # this class is agnostic about the dossier location
        # we may interrogate multiple times 
        # producing multiple dossiers

        with open(dossierfile,'r') as f:
            unordereddossier = {line.strip() for line in f}

        # return type is a set containing text
        # permits comparison without regard to order
        # python uses hash based lookups
        # several million elements are fine
        return unordereddossier

    def _getesrievidence(self
                        ,columns 
                        ,dossierfile 
                        ,shapecolumn=None
                        ,rounddigits=1
                        ,convertfactor=1
                        ,whereclause=None):

        columnlist, shape_index = self._getcolumninfo(columns
                                                     ,shapecolumn)

        with open(dossierfile, 'w') as f: 
            try:
                with arcpy.da.SearchCursor(self.layer
                                          ,columnlist
                                          ,where_clause=whereclause) as cursor:
                    for row in cursor:

                        # convert tuple to list
                        row = list(row)

                        if  shape_index is not None \
                        and convertfactor != 1:
                            row = self._convertrow(row
                                                ,shape_index
                                                ,convertfactor)
                        
                        if shape_index is not None:
                            row = self._roundrow(row
                                                ,shape_index
                                                ,rounddigits)

                        # write the evidence to the dossier
                        f.write(",".join(str(item) for item in row) + "\n")
            except Exception as e:
                print('Error opening SearchCursor for')
                print('   layer: {0}'.format(self.layer))
                print('   columnlist: {0}'.format(columnlist))
                print('   where clause: {0}'.format(whereclause))
                raise ValueError(traceback.format_exc())

    def _getcolumninfo(self
                      ,columns
                      ,shapecolumn):

        # convert comma-delimited columns to list
        # get shape index of the list if it exists
        # this is shared by all children

        columnlist = [f.strip() for f in columns.split(",")]

        # we support rounding and converting one column only (for now (forever?))
        try:
            shape_index = columnlist.index(shapecolumn)
        except ValueError:
            shape_index = None

        return columnlist, shape_index

    def _convertrow(self
                   ,row
                   ,rowindex
                   ,convertfactor):

        # convert sq m to sq feet for example
        # that type of conversion
        # TODO: any tests for this?

        if isinstance(row[rowindex], (float, int)):
            row[rowindex] = row[rowindex] * convertfactor
        
        return row

    def _isfloatable(self
                   ,input):
        try:
            float(input)
            return True 
        except ValueError:
            return False

    def _roundrow(self
                 ,row
                 ,rowindex
                 ,rounddigits):

        # fish out the rounding column position and round if its a number
        # reminder: round now as number
        #           later write to dossier. dossier is a set of text

        if isinstance(row[rowindex], (tuple)): 

            # for points we will typically request (x,y) instead of area/length
            # arcpy search cursor returns these as tuples
            # goes first, dont let it fall into the next elif
            # ToDo gotta think about PostGIS here

            if rounddigits > 0:
                row[rowindex] = tuple(round(num, rounddigits) for num in row[rowindex])
            else:
                row[rowindex] = tuple(int(round(num, rounddigits)) for num in row[rowindex])

        elif isinstance(row[rowindex], (float, int)) \
        or  (isinstance(row[rowindex], (str)) and self._isfloatable(row[rowindex])):    
                        
            if rounddigits > 0:
                row[rowindex] = round(float(row[rowindex]), rounddigits)
            else:
                # rounding floats produces floats like 
                # round(123.123,-1) = 120.0 
                # so int() to produce the more expected 120
                row[rowindex] = int(round(float(row[rowindex]), rounddigits))

        return row


class csclfeatureclass(suspects):

    def __init__(self
                ,gdb
                ,layer):

        # file geodatabase or enterprise geodatabase
        self.gdb    = gdb
        self.layer  = layer

    def getevidence(self
                   ,columns 
                   ,dossierfile 
                   ,shapecolumn=None
                   ,rounddigits=1
                   ,convertfactor=1
                   ,whereclause=None):

        arcpy.env.workspace = self.gdb

        super()._getesrievidence(columns 
                                ,dossierfile 
                                ,shapecolumn
                                ,rounddigits
                                ,convertfactor
                                ,whereclause)

        arcpy.env.workspace = None
    

class hostedfeaturelayer(suspects):

    def __init__(self
                ,url
                ,layer):

        # layer name is determined by caller not by agol
        # use it to instantiate a unique name in 
        # our current arcpy session

        self.url    = url   
        self.layer  = layer

        arcpy.MakeFeatureLayer_management(self.url
                                         ,self.layer)   

    def getevidence(self
                   ,columns 
                   ,dossierfile 
                   ,shapecolumn=None
                   ,rounddigits=1
                   ,convertfactor=1
                   ,whereclause=None):     

        super()._getesrievidence(columns 
                                ,dossierfile 
                                ,shapecolumn
                                ,rounddigits
                                ,convertfactor
                                ,whereclause)


class postgistable(suspects):

    def __init__(self
                ,database
                ,table):
        
        self.pgdatabase = database
        self.table      = table
        self.pghost     = os.getenv('PGHOST', 'localhost')
        self.pgport     = os.getenv('PGPORT', 5432)    

    def getevidence(self
                   ,columns
                   ,dossierfile
                   ,shapecolumn=None
                   ,rounddigits=1
                   ,convertfactor=1
                   ,whereclause=None):

        columnlist, shape_index = super()._getcolumninfo(columns
                                                        ,shapecolumn)

        with open(dossierfile, 'w') as f: 

            # list of lists
            rows = self._getrows(columns
                                ,whereclause)

            for row in rows:

                if  shape_index is not None \
                and convertfactor != 1:
                    row = super()._convertrow(row
                                             ,shape_index
                                             ,convertfactor)
                
                if shape_index is not None:
                    row = super()._roundrow(row
                                           ,shape_index
                                           ,rounddigits)

                # write the evidence to the dossier
                f.write(",".join(str(item) for item in row) + "\n")

    def _getrows(self
                ,columns
                ,whereclause):

        # this is the postgis class equivalent of 
        # arcpy.da.SearchCursor in the esri classes
        
        sql = "select {0} from {1}".format(columns
                                          ,self.table)

        if whereclause:
            sql += """ where {0} """.format(whereclause)

        # tuples only, ignore user startup file, unaligned output   
        # except for database, connection is externalized   
        psqlcmd = 'psql -d {0} -F {1} -tXA -c "{2}" '.format(self.pgdatabase
                                                            ,','
                                                            ,sql)
        
        try:
            p1 = subprocess.Popen(psqlcmd
                                 ,stdout=subprocess.PIPE
                                 ,stderr=subprocess.PIPE
                                 ,shell=True
                                 ,text=True) #return strings not bytes

            # outputstr is a big chunk of text
            outputstr, error = p1.communicate()

            if p1.returncode != 0:
                raise ValueError(
                    "psql call to database {0} failed using {1}.\n"
                    "Returncode is {2} error is {3}".format(self.pgdatabase
                                                           ,psqlcmd
                                                           ,p1.returncode
                                                           ,error))
        except Exception as e:
            raise ValueError(
                    "Exception occurred while running command {0}.\n" 
                    "Exception: {1}".format(psqlcmd
                                           ,str(e)))

        # convert to a list with one row per element
        rows = [line.split(',') for line in outputstr.strip().splitlines()]

        # [['Queens', '4'], ['Manhattan', '5']]
        # the commas are standard python pretty-print

        return self._tuplepoints(rows)

    def _tuplepoints(self
                    ,listofrows):

        # we use x,y for points in lieu of shape_area or shape_length
        # esri @SHAPEXY   returns tuple (1.23 4.56)
        # st_astext(geom) returns POINT(1.23, 4.56)

        pattern = r'^POINT\((-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\)$'

        for i in range(len(listofrows)):

            for j in range(len(listofrows[i])):

                match = re.match(pattern, listofrows[i][j])

                if match:
                    x,y = match.groups()
                    listofrows[i][j] = (float(x), float(y))

        return listofrows




        

