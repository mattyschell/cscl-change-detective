import unittest
import os
import subprocess
import time

import interrogator

class InterrogatorPolyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):


        cls.testdatabase = 'csclchangedetective'
        cls.testlayer   = 'borough'
        cls.testcolumn1 = 'boroname'
        cls.testcolumn2 = 'county'
        cls.testcolumn3 = 'shape_area'

        cls.testdossierfile = os.path.join(os.path.dirname(__file__)
                                          ,'testdata'
                                          ,'testdossier')

        cls.borough = interrogator.postgistable(cls.testdatabase
                                               ,cls.testlayer)

        cls.teardownsql = './src/py/testdata/sql/teardown.sql'
        cls.schemasql   = './src/py/testdata/sql/schema.sql'
        cls.datasql     = './src/py/testdata/sql/data.sql'

        os.environ["PGDATABASE"] = 'postgres'
        os.environ["PGUSER"] = 'postgres'
        subprocess.run(["psql", "-f", cls.schemasql], check=True)

        os.environ["PGDATABASE"] = cls.testdatabase
        subprocess.run(["psql", "-f", cls.datasql], check=True)

        # not real only exist temporarily for scratch setup and teardown
        cls.superpw = os.environ["PGPASSWORD"]
        os.environ["PGUSER"] = 'carmensandiego'
        os.environ["PGPASSWORD"] = 'appleII3'

    @classmethod
    def tearDownClass(cls):

        os.environ["PGPASSWORD"] = cls.superpw
        os.environ["PGDATABASE"] = 'postgres'
        os.environ['PGUSER']     = 'postgres'
        subprocess.run(["psql", "-f", cls.teardownsql], check=True)       
        
    def tearDown(self):

        try:
            os.remove(self.testdossierfile)
        except FileNotFoundError:
            pass

    def test_agetevidence(self):
        
        self.borough.getevidence(self.testcolumn1
                                ,self.testdossierfile)

        self.assertTrue(os.path.isfile(self.testdossierfile))

    

if __name__ == '__main__':
    unittest.main()