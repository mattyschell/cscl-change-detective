import unittest
import os
import subprocess
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'py'))
import interrogator

class InterrogatorPointTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.testdatabase = 'csclchangedetective'
        cls.testlayer    = 'MilePost'
        cls.testcolumn1  = 'milepostid'
        cls.testcolumn2  = 'routeid'
        # mimic arcpy token SHAPE@XY
        cls.testcolumn3  = 'st_astext(geom)'

        cls.testdossierfile = os.path.join(os.path.dirname(__file__)
                                          ,'testdata'
                                          ,'testdossier')

        cls.milepost = interrogator.postgistable(cls.testdatabase
                                                ,cls.testlayer)

        cls.teardownsql = './test/testdata/sql/teardown.sql'
        cls.schemasql   = './test/testdata/sql/schema.sql'
        # includes borough and milepost
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

        self.milepost.getevidence(self.testcolumn1
                                 ,self.testdossierfile)

        self.assertTrue(os.path.isfile(self.testdossierfile))

    def test_bfailtogetevidence(self):
        
        with self.assertRaises(ValueError):
            self.milepost.getevidence('SpreadLoveItsTheBrooklynWay'
                                     ,self.testdossierfile)

    def test_cgetmoreevidence(self):

        self.milepost.getevidence('{0},{1}'.format(self.testcolumn1
                                                  ,self.testcolumn2)
                                  ,self.testdossierfile)

        self.assertTrue(os.path.isfile(self.testdossierfile))

    def test_daddshape(self):

        self.milepost.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                      ,self.testcolumn2
                                                      ,self.testcolumn3)
                                 ,self.testdossierfile)

        self.assertTrue(os.path.isfile(self.testdossierfile))

    def test_egetshapedossier(self):

        expecteddossier = {"1,95I,(1037085.7034301758, 262114.19799804688)"
                          ,"2,95I,(1030095.9494018555, 257745.85382080078)"
                          ,"3,95I,(1031671.8986206055, 253286.89581298828)"
                          ,"4,95I,(1031927.9490356445, 252819.0751953125)"
                          ,"5,95I,(1031187.4111938477, 254226.90600585938)"}

        self.milepost.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                      ,self.testcolumn2
                                                      ,self.testcolumn3)
                                 ,self.testdossierfile)

        self.assertEqual(self.milepost.getdossier(self.testdossierfile)
                        ,expecteddossier)

    def test_froundshape(self):

        expecteddossier = {"1,95I,(1037085.7, 262114.2)"
                          ,"2,95I,(1030095.9, 257745.9)"
                          ,"3,95I,(1031671.9, 253286.9)"
                          ,"4,95I,(1031927.9, 252819.1)"
                          ,"5,95I,(1031187.4, 254226.9)"}

        self.milepost.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                      ,self.testcolumn2
                                                      ,self.testcolumn3)
                                 ,self.testdossierfile
                                 ,self.testcolumn3)

        self.assertEqual(self.milepost.getdossier(self.testdossierfile)
                        ,expecteddossier)

    def test_froundtensshape(self):

        expecteddossier = {"1,95I,(1037090, 262110)"
                          ,"2,95I,(1030100, 257750)"
                          ,"3,95I,(1031670, 253290)"
                          ,"4,95I,(1031930, 252820)"
                          ,"5,95I,(1031190, 254230)"}

        self.milepost.getevidence('{0},{1},{2}'.format(self.testcolumn1
                                                      ,self.testcolumn2
                                                      ,self.testcolumn3)
                                 ,self.testdossierfile
                                 ,self.testcolumn3
                                 ,-1)

        self.assertEqual(self.milepost.getdossier(self.testdossierfile)
                        ,expecteddossier)

    def test_hroundwholedossier(self):

        expecteddossier = {"1,95I,(1037086, 262114)"
                          ,"2,95I,(1030096, 257746)"
                          ,"3,95I,(1031672, 253287)"
                          ,"4,95I,(1031928, 252819)"
                          ,"5,95I,(1031187, 254227)"}


if __name__ == '__main__':
    unittest.main()