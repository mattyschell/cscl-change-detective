import unittest
import os

import interrogator

class InterrogatorTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.testgdb = os.path.join(os.path.dirname(__file__)
                                   ,'testdata'
                                   ,'test.gdb')

        cls.testlayer   = 'MilePost'
        cls.testcolumn1 = 'MILEPOSTID'
        # field tokens. POINT_X POINT_Y also exist but challenging
        # SHAPE@XY returns a tuple (123,456) 
        cls.testcolumn2 = 'SHAPE@XY'

        cls.testdossierfile = os.path.join(os.path.dirname(__file__)
                                          ,'testdata'
                                          ,'testdossier')

        cls.milepost = interrogator.csclitem(cls.testgdb
                                            ,cls.testlayer)

    def tearDown(self):

        try:
            os.remove(self.testdossierfile)
        except FileNotFoundError:
            pass

    def test_agetevidence(self):

        self.milepost.getevidence(self.testcolumn1
                                 ,self.testdossierfile)

        self.assertTrue(os.path.isfile(self.testdossierfile))

    def test_bgetxy(self):

        self.milepost.getevidence(self.testcolumn2
                                 ,self.testdossierfile)

        self.assertTrue(os.path.isfile(self.testdossierfile))

    def test_cgetdossier(self):

        expecteddossier = {"3,(1031671.8986206055, 253286.89581298828)"
                          ,"4,(1031927.9490356445, 252819.0751953125)"
                          ,"1,(1037085.7034301758, 262114.19799804688)"
                          ,"2,(1030095.9494018555, 257745.85382080078)"
                          ,"5,(1031187.4111938477, 254226.90600585938)"}

        self.milepost.getevidence('{0},{1}'.format(self.testcolumn1
                                                  ,self.testcolumn2)
                                ,self.testdossierfile)

        self.assertEqual(self.milepost.getdossier(self.testdossierfile)
                        ,expecteddossier)


        

if __name__ == '__main__':
    unittest.main()