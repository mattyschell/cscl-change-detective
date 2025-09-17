import unittest
import os

import interrogator

class InterrogatorTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.testgdb = os.path.join(os.path.dirname(__file__)
                                   ,'testdata'
                                   ,'test.gdb')

        cls.testlayer   = 'Borough'
        cls.testcolumn1 = 'BORONAME'
        cls.testcolumn2 = 'COUNTY'
        cls.testcolumn3 = 'Shape_Area'

        cls.testdossier = os.path.join(os.path.dirname(__file__)
                                       ,'testdata'
                                       ,'testdossier')

        cls.borough = interrogator.csclitem(cls.testgdb
                                           ,cls.testlayer)

    def tearDown(self):

        try:
            os.remove(self.testdossier)
        except FileNotFoundError:
            pass

    def test_agetevidence(self):

        self.borough.getevidence(self.testcolumn1
                                ,self.testdossier)

        self.assertTrue(os.path.isfile(self.testdossier))

    def test_bgetmoreevidence(self):

        self.borough.getevidence('{0},{1}'.format(self.testcolumn1
                                                 ,self.testcolumn2)
                                ,self.testdossier)

    def test_caddshape(self):

        # area tells us a lot about shape
        # todo: will need to deal with precision and units 

        self.borough.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                     ,self.testcolumn2
                                                     ,self.testcolumn3)
                                ,self.testdossier)

        self.assertTrue(os.path.isfile(self.testdossier))


    def test_dgetdossier(self):

        expecteddossier = {"Queens,Queens,4962897934.05186"
                          ,"Manhattan,New York,944328629.691523"
                          ,"Bronx,Bronx,1598501138.43022"
                          ,"Brooklyn,Kings,2697660950.436"
                          ,"Staten Island,Richmond,2851517714.98682"}

        self.borough.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                     ,self.testcolumn2
                                                     ,self.testcolumn3)
                                ,self.testdossier)

        self.assertEqual(self.borough.getdossier()
                        ,expecteddossier)


        

if __name__ == '__main__':
    unittest.main()