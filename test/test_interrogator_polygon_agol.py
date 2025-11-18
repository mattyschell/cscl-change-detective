import unittest
import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'py'))
import interrogator

class InterrogatorPolyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.testurl = 'https://services6.arcgis.com/yG5s3afENB5iO9fj/arcgis/rest/services/Borough_view/FeatureServer/0'
        
        cls.testlayer   = 'Borough'
        cls.testcolumn1 = 'BORONAME'
        cls.testcolumn2 = 'COUNTY'

        # hosted feature layers add an underscore to avoid conflicts with storage layers
        # usualy these are lousy web mercator and worthless
        cls.areacolumn = 'SHAPE__Area'
        # centroid
        cls.centroidcalculated = 'SHAPE@XY'

        cls.testdossierfile = os.path.join(os.path.dirname(__file__)
                                          ,'testdata'
                                          ,'testdossier')

        cls.borough = interrogator.hostedfeaturelayer(cls.testurl
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

        self.borough.getevidence('{0}|||{1}'.format(self.testcolumn1
                                                   ,self.testcolumn2)
                                ,self.testdossierfile)

        self.assertTrue(os.path.isfile(self.testdossierfile))
        
    def test_caddshape(self):

        self.borough.getevidence('{0}|||{1}|||{2}'.format(self.testcolumn1
                                                         ,self.testcolumn2
                                                         ,self.areacolumn)
                                ,self.testdossierfile)

        self.assertTrue(os.path.isfile(self.testdossierfile))

    def test_dgetdossier(self):

        # area in square meters
        expecteddossier = {"Staten Island,Richmond,459489372.20703125"
                          ,"Bronx,Bronx,259796496.62890625"
                          ,"Queens,Queens,801990330.7890625"
                          ,"Brooklyn,Kings,435630776.72265625"
                          ,"Manhattan,New York,153133552.01171875"}           

        self.borough.getevidence('{0}|||{1}|||{2}'.format(self.testcolumn1
                                                         ,self.testcolumn2
                                                         ,self.areacolumn)
                                ,self.testdossierfile)

        self.assertEqual(self.borough.getdossier(self.testdossierfile)
                        ,expecteddossier)

    def test_drounddossier(self):
                    
        expecteddossier = {"Staten Island,Richmond,459489372"
                          ,"Bronx,Bronx,259796497"
                          ,"Queens,Queens,801990331"
                          ,"Brooklyn,Kings,435630777"
                          ,"Manhattan,New York,153133552"}           

        self.borough.getevidence('{0}|||{1}|||{2}'.format(self.testcolumn1
                                                         ,self.testcolumn2
                                                         ,self.areacolumn)
                                ,self.testdossierfile
                                ,self.areacolumn
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
                                                   
        self.borough.getevidence('{0}|||{1}|||{2}'.format(self.testcolumn1
                                                         ,self.testcolumn2
                                                         ,self.areacolumn)
                                ,self.testdossierfile
                                ,self.areacolumn
                                ,0
                                ,10.7639104)

        self.assertEqual(self.borough.getdossier(self.testdossierfile)
                        ,expecteddossier)

    def test_fwhereclause(self):

        expecteddossier = {"Queens,Queens,801990330.8"}

        testwhereclause = "BORONAME = 'Queens'"

        self.borough.getevidence('{0}|||{1}|||{2}'.format(self.testcolumn1
                                                         ,self.testcolumn2
                                                         ,self.areacolumn)
                                ,self.testdossierfile
                                ,self.areacolumn
                                ,whereclause=testwhereclause)

        self.assertEqual(self.borough.getdossier(self.testdossierfile)
                        ,expecteddossier)

        testwhereclause = "Shape__Area > 800000000"

        self.borough.getevidence('{0}|||{1}|||{2}'.format(self.testcolumn1
                                                         ,self.testcolumn2
                                                         ,self.areacolumn)
                                ,self.testdossierfile
                                ,self.areacolumn
                                ,whereclause=testwhereclause)

        self.assertEqual(self.borough.getdossier(self.testdossierfile)
                        ,expecteddossier)

        expecteddossier = set()
        testwhereclause = "BORONAME = 'Philadelphia'"

        self.borough.getevidence('{0}|||{1}|||{2}'.format(self.testcolumn1
                                                         ,self.testcolumn2
                                                         ,self.areacolumn)
                                ,self.testdossierfile
                                ,self.areacolumn
                                ,whereclause=testwhereclause)

        self.assertEqual(self.borough.getdossier(self.testdossierfile)
                        ,expecteddossier)

    def test_gcalccentroid(self):

        #expected
        #select boroname 
        #	|| ',(' 
        #	|| ROUND(SDO_GEOM.SDO_CENTROID(sdo_cs.transform(
        #              SDO_GEOM.SDO_ARC_DENSIFY(a.shape, .005, 'arc_tolerance=0.5 unit=foot')
        #                       ,3857)).sdo_point.x
        #             , -1) 
        #	|| ', ' 
        #	|| ROUND(SDO_GEOM.SDO_CENTROID(sdo_cs.transform(
        #              SDO_GEOM.SDO_ARC_DENSIFY(a.shape, .005, 'arc_tolerance=0.5 unit=foot')
        #                       ,3857)).sdo_point.y
        #            ,-1)
        #	|| ')'
        #from 
        #	cscl_pub.borough a

        expecteddossier = {"Staten Island,(-8253040, 4948010)"
                          ,"Queens,(-8219690, 4961980)"
                          ,"Brooklyn,(-8232090, 4958560)"
                          ,"Bronx,(-8221300, 4990130)"
                          ,"Manhattan,(-8234290, 4979110)"}

        # in this particular case the Y value differs by 1 foot for 4 of the boroughs
        # rounding to tens place is not strictly necessary. just a reminder to self 
        self.borough.getevidence('{0}|||{1}'.format(self.testcolumn1
                                                   ,self.centroidcalculated)
                                ,self.testdossierfile
                                ,self.centroidcalculated
                                ,-1) 

        self.assertEqual(self.borough.getdossier(self.testdossierfile)
                        ,expecteddossier)

if __name__ == '__main__':
    unittest.main()