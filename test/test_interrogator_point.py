import unittest
import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'py'))
import interrogator

class InterrogatorPointTestCase(unittest.TestCase):

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

        cls.milepost = interrogator.csclfeatureclass(cls.testgdb
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

    def test_drounddossier(self):

        expecteddossier = {"3,(1031671.9, 253286.9)"
                          ,"4,(1031927.9, 252819.1)"
                          ,"1,(1037085.7, 262114.2)"
                          ,"2,(1030095.9, 257745.9)"
                          ,"5,(1031187.4, 254226.9)"}

        self.milepost.getevidence('{0},{1}'.format(self.testcolumn1
                                                  ,self.testcolumn2)
                                ,self.testdossierfile
                                ,self.testcolumn2)

        self.assertEqual(self.milepost.getdossier(self.testdossierfile)
                        ,expecteddossier)

    def test_droundtensdossier(self):

        expecteddossier = {"3,(1031670, 253290)"
                          ,"4,(1031930, 252820)"
                          ,"1,(1037090, 262110)"
                          ,"2,(1030100, 257750)"
                          ,"5,(1031190, 254230)"}

        self.milepost.getevidence('{0},{1}'.format(self.testcolumn1
                                                  ,self.testcolumn2)
                                ,self.testdossierfile
                                ,self.testcolumn2
                                ,-1)

        self.assertEqual(self.milepost.getdossier(self.testdossierfile)
                        ,expecteddossier)

if __name__ == '__main__':
    unittest.main()