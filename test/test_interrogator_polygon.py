import unittest
import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'py'))
import interrogator

class InterrogatorPolyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.testgdb = os.path.join(os.path.dirname(__file__)
                                   ,'testdata'
                                   ,'test.gdb')

        cls.testlayer   = 'Borough'
        cls.testcolumn1 = 'BORONAME'
        cls.testcolumn2 = 'COUNTY'
        # KISS - iterrogator should know if we are doing area, pointxy, etc
        # this could also be SHAPE.AREA
        # the casing does not seem to matter. not sure what the pattern is, weird
        cls.testcolumn3 = 'Shape_Area'

        cls.testdossierfile = os.path.join(os.path.dirname(__file__)
                                          ,'testdata'
                                          ,'testdossier')

        cls.borough = interrogator.csclfeatureclass(cls.testgdb
                                                   ,cls.testlayer)

    def tearDown(self):

        try:
            os.remove(self.testdossierfile)
        except FileNotFoundError:
            pass

    def test_agetevidence(self):

        self.borough.getevidence(self.testcolumn1
                                ,self.testdossierfile)

        self.assertTrue(os.path.isfile(self.testdossierfile))

    def test_bgetmoreevidence(self):

        self.borough.getevidence('{0},{1}'.format(self.testcolumn1
                                                 ,self.testcolumn2)
                                ,self.testdossierfile)

        self.assertTrue(os.path.isfile(self.testdossierfile))

    def test_caddshape(self):

        self.borough.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                     ,self.testcolumn2
                                                     ,self.testcolumn3)
                                ,self.testdossierfile)

        self.assertTrue(os.path.isfile(self.testdossierfile))

    def test_dgetdossier(self):

        expecteddossier = {"Queens,Queens,4962897934.05186"
                          ,"Manhattan,New York,944328629.691523"
                          ,"Bronx,Bronx,1598501138.43022"
                          ,"Brooklyn,Kings,2697660950.436"
                          ,"Staten Island,Richmond,2851517714.98682"}
                          

        self.borough.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                     ,self.testcolumn2
                                                     ,self.testcolumn3)
                                ,self.testdossierfile)

        self.assertEqual(self.borough.getdossier(self.testdossierfile)
                        ,expecteddossier)

    def test_erounddossier(self):

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

    def test_froundtensdossier(self):
                                          
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

    def test_groundwholedossier(self):

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