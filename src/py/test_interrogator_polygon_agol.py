import unittest
import os

import interrogator

class InterrogatorPolyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.testurl = 'https://services6.arcgis.com/yG5s3afENB5iO9fj/arcgis/rest/services/Borough_view/FeatureServer/0'
        
        cls.testlayer   = 'Borough'
        cls.testcolumn1 = 'BORONAME'
        cls.testcolumn2 = 'COUNTY'
        # hosted feature layers add an underscore to avoid conflicts with storage layers
        cls.testcolumn3 = 'SHAPE__Area'

        cls.testdossierfile = os.path.join(os.path.dirname(__file__)
                                          ,'testdata'
                                          ,'testdossier')

        cls.borough = interrogator.hostedfeaturelayer(cls.testurl
                                                     ,cls.testlayer)

        # thats right
        #cls.agol_fudge_factor = 1/1.745489                   

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

        # area in square meters
        expecteddossier = {"Staten Island,Richmond,459489372.20703125"
                          ,"Bronx,Bronx,259796496.62890625"
                          ,"Queens,Queens,801990330.7890625"
                          ,"Brooklyn,Kings,435630776.72265625"
                          ,"Manhattan,New York,153133552.01171875"}           

        self.borough.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                     ,self.testcolumn2
                                                     ,self.testcolumn3)
                                ,self.testdossierfile)

        self.assertEqual(self.borough.getdossier(self.testdossierfile)
                        ,expecteddossier)

    def test_drounddossier(self):
                    
        expecteddossier = {"Staten Island,Richmond,459489372"
                          ,"Bronx,Bronx,259796497"
                          ,"Queens,Queens,801990331"
                          ,"Brooklyn,Kings,435630777"
                          ,"Manhattan,New York,153133552"}           

        self.borough.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                     ,self.testcolumn2
                                                     ,self.testcolumn3)
                                ,self.testdossierfile
                                ,self.testcolumn3
                                ,0)

        self.assertEqual(self.borough.getdossier(self.testdossierfile)
                        ,expecteddossier)

    def test_eroundsquarefeetdossier(self):

        # AGOL output converted with a calculator
        expecteddossier = {"Queens,Queens,8632552062"
                          ,"Manhattan,New York,1648315833"
                          ,"Bronx,Bronx,2796426212"
                          ,"Brooklyn,Kings,4689090648"
                          ,"Staten Island,Richmond,4945902432"}
                                                   
        self.borough.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                     ,self.testcolumn2
                                                     ,self.testcolumn3)
                                ,self.testdossierfile
                                ,self.testcolumn3
                                ,0
                                ,10.7639104)

        self.assertEqual(self.borough.getdossier(self.testdossierfile)
                        ,expecteddossier)

#    def test_fmatchcscldossier(self):
#        # converting square meters to square feet should match
#        # the file geodatabase in this repo (with sufficient rounding)
#        # owever AGOL Shape__Area values are being calculated in loust web mercator
#        # for now we have no solution
#        expecteddossier = {"Queens,Queens,4962900000"
#                          ,"Manhattan,New York,944330000"
#                          ,"Bronx,Bronx,1598500000"
#                          ,"Brooklyn,Kings,2697660000"
#                          ,"Staten Island,Richmond,2851520000"}
#                                                   
#        self.borough.getevidence('{0},{1},{2}'.format(self.testcolumn1
#                                                     ,self.testcolumn2
#                                                     ,self.testcolumn3)
#                                ,self.testdossierfile
#                                ,self.testcolumn3
#                                ,-4
#                                ,(10.7639104 * self.agol_fudge_factor))
#
#        self.assertEqual(self.borough.getdossier(self.testdossierfile)
#                        ,expecteddossier)
#

    def test_gwhereclause(self):

        expecteddossier = {"Queens,Queens,801990330.8"}

        testwhereclause = "BORONAME = 'Queens'"

        self.borough.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                     ,self.testcolumn2
                                                     ,self.testcolumn3)
                                ,self.testdossierfile
                                ,self.testcolumn3
                                ,whereclause=testwhereclause)

        self.assertEqual(self.borough.getdossier(self.testdossierfile)
                        ,expecteddossier)

        testwhereclause = "Shape__Area > 800000000"

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