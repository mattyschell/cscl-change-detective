import unittest
import os
import subprocess

import interrogator

class InterrogatorPolyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.testdatabase = 'csclchangedetective'
        cls.testlayer   = 'Borough'
        cls.testcolumn1 = 'BORONAME'
        cls.testcolumn2 = 'COUNTY'
        # hosted feature layers add an underscore to avoid conflicts with storage layers
        cls.testcolumn3 = 'SHAPE__Area'

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

    @classmethod
    def tearDownClass(cls):

        os.environ["PGDATABASE"] = 'postgres'
        subprocess.run(["psql", "-f", cls.teardownsql], check=True)       

    def tearDown(self):

        try:
            os.remove(self.testdossierfile)
        except FileNotFoundError:
            pass



    def test_agetevidence(self):

        pass
        #self.borough.getevidence(self.testcolumn1
        #                        ,self.testdossierfile)

        #self.assertTrue(os.path.isfile(self.testdossierfile))

    

if __name__ == '__main__':
    unittest.main()