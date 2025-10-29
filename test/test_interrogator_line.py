import unittest
import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'py'))
import interrogator

class InterrogatorLineTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.testgdb = os.path.join(os.path.dirname(__file__)
                                   ,'testdata'
                                   ,'test.gdb')

        cls.testlayer   = 'Subway'
        cls.testcolumn1 = 'SEGMENTID'
        # Could also be SHAPE.LEN
        # casing is chaotic but doesnt seem to matter
        cls.testcolumn2 = 'SHAPE_Length'

        cls.testdossierfile = os.path.join(os.path.dirname(__file__)
                                          ,'testdata'
                                          ,'testdossier')

        cls.subway = interrogator.csclfeatureclass(cls.testgdb
                                                  ,cls.testlayer)

    def tearDown(self):

        try:
            os.remove(self.testdossierfile)
        except FileNotFoundError:
            pass

    def test_agetevidence(self):

        self.subway.getevidence(self.testcolumn1
                               ,self.testdossierfile)

        self.assertTrue(os.path.isfile(self.testdossierfile))

    def test_baddshape(self):

        self.subway.getevidence('{0},{1}'.format(self.testcolumn1
                                                ,self.testcolumn2)
                                ,self.testdossierfile)

        self.assertTrue(os.path.isfile(self.testdossierfile))

    def test_cgetdossier(self):

        expecteddossier = {"8100837,646.2074999419764"
                          ,"8100834,259.53218856455356"
                          ,"8100835,97.73967979224953"
                          ,"8100838,262.6696706688732"
                          ,"8100836,287.4570346063792"}

        self.subway.getevidence('{0},{1}'.format(self.testcolumn1
                                                ,self.testcolumn2)
                                ,self.testdossierfile)

        self.assertEqual(self.subway.getdossier(self.testdossierfile)
                        ,expecteddossier)

    def test_drounddossier(self):

        expecteddossier = {"8100837,646.2"
                          ,"8100834,259.5"
                          ,"8100835,97.7"
                          ,"8100838,262.7"
                          ,"8100836,287.5"}

        self.subway.getevidence('{0},{1}'.format(self.testcolumn1
                                                ,self.testcolumn2)
                                ,self.testdossierfile
                                ,self.testcolumn2)

        self.assertEqual(self.subway.getdossier(self.testdossierfile)
                        ,expecteddossier)

        

if __name__ == '__main__':
    unittest.main()