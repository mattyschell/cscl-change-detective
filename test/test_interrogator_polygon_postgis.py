import unittest
import os
import subprocess
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'py'))
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

        cls.teardownsql = './test/testdata/sql/teardown.sql'
        cls.schemasql   = './test/testdata/sql/schema.sql'
        cls.datasql     = './test/testdata/sql/data.sql'

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

    def test_bfailtogetevidence(self):
        
        with self.assertRaises(ValueError):
            self.borough.getevidence('SpreadLoveItsTheBrooklynWay'
                                    ,self.testdossierfile)

    def test_cgetmoreevidence(self):

        self.borough.getevidence('{0},{1}'.format(self.testcolumn1
                                                 ,self.testcolumn2)
                                ,self.testdossierfile)

        self.assertTrue(os.path.isfile(self.testdossierfile))

    def test_daddshape(self):

        self.borough.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                     ,self.testcolumn2
                                                     ,self.testcolumn3)
                                ,self.testdossierfile)

        self.assertTrue(os.path.isfile(self.testdossierfile))
    
    def test_egetdossier(self):

        expecteddossier = {"Queens,Queens,4962897934.05"
                          ,"Manhattan,New York,944328629.692"
                          ,"Bronx,Bronx,1598501138.43"
                          ,"Brooklyn,Kings,2697660950.44"
                          ,"Staten Island,Richmond,2851517714.99"}
                          
        self.borough.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                     ,self.testcolumn2
                                                     ,self.testcolumn3)
                                ,self.testdossierfile)

        self.assertEqual(self.borough.getdossier(self.testdossierfile)
                        ,expecteddossier)

    def test_frounddossier(self):

        expecteddossier = {"Queens,Queens,4962897934.1"
                          ,"Manhattan,New York,944328629.7"
                          ,"Bronx,Bronx,1598501138.4"
                          ,"Brooklyn,Kings,2697660950.4"
                          ,"Staten Island,Richmond,2851517715.0"}

        self.borough.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                     ,self.testcolumn2
                                                     ,self.testcolumn3)
                                ,self.testdossierfile
                                ,self.testcolumn3)

        self.assertEqual(self.borough.getdossier(self.testdossierfile)
                        ,expecteddossier)

    def test_groundtensdossier(self):
                                          
        expecteddossier = {"Queens,Queens,4962897930"
                          ,"Manhattan,New York,944328630"
                          ,"Bronx,Bronx,1598501140"
                          ,"Brooklyn,Kings,2697660950"
                          ,"Staten Island,Richmond,2851517710"} 

        self.borough.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                     ,self.testcolumn2
                                                     ,self.testcolumn3)
                                ,self.testdossierfile
                                ,self.testcolumn3
                                ,-1)

        self.assertEqual(self.borough.getdossier(self.testdossierfile)
                        ,expecteddossier)

    def test_hroundwholedossier(self):

        expecteddossier = {"Queens,Queens,4962897934"
                          ,"Manhattan,New York,944328630"
                          ,"Bronx,Bronx,1598501138"
                          ,"Brooklyn,Kings,2697660950"
                          ,"Staten Island,Richmond,2851517715"}

        self.borough.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                     ,self.testcolumn2
                                                     ,self.testcolumn3)
                                ,self.testdossierfile
                                ,self.testcolumn3
                                ,0)

        self.assertEqual(self.borough.getdossier(self.testdossierfile)
                        ,expecteddossier)

    def test_hwhereclause(self):

        expecteddossier = {"Queens,Queens,4962897934.1"}

        testwhereclause = "BORONAME = 'Queens'"

        self.borough.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                     ,self.testcolumn2
                                                     ,self.testcolumn3)
                                ,self.testdossierfile
                                ,self.testcolumn3
                                ,whereclause=testwhereclause)

        self.assertEqual(self.borough.getdossier(self.testdossierfile)
                        ,expecteddossier)

        testwhereclause = "Shape_Area > 4000000000"

        self.borough.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                     ,self.testcolumn2
                                                     ,self.testcolumn3)
                                ,self.testdossierfile
                                ,self.testcolumn3
                                ,whereclause=testwhereclause)

        self.assertEqual(self.borough.getdossier(self.testdossierfile)
                        ,expecteddossier)

        expecteddossier = set()
        testwhereclause = "BORONAME = 'Philadelphia'"

        self.borough.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                     ,self.testcolumn2
                                                     ,self.testcolumn3)
                                ,self.testdossierfile
                                ,self.testcolumn3
                                ,whereclause=testwhereclause)

        self.assertEqual(self.borough.getdossier(self.testdossierfile)
                        ,expecteddossier)

if __name__ == '__main__':
    unittest.main()