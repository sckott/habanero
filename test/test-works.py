"""Tests for GNI module of habanero"""
import os
from habanero import Habanero
hb = Habanero()

a = '{"status":"ok","message-type":"work","message-version":"1.0.0","message":{"indexed":{"date-parts":[[2015,6,9]],"timestamp":1433817308344},"reference-count":0,"publisher":"Public Library of Science (PLoS)","issue":"3","DOI":"10.1371\\/journal.pone.0033693","type":"journal-article","page":"e33693","update-policy":"http:\\/\\/dx.doi.org\\/10.1371\\/journal.pone.corrections_policy","source":"CrossRef","title":["Methylphenidate Exposure Induces Dopamine Neuron Loss and Activation of Microglia in the Basal Ganglia of Mice"],"prefix":"http:\\/\\/id.crossref.org\\/prefix\\/10.1371","volume":"7","author":[{"affiliation":[],"family":"Sadasivan","given":"Shankar"},{"affiliation":[],"family":"Pond","given":"Brooks B."},{"affiliation":[],"family":"Pani","given":"Amar K."},{"affiliation":[],"family":"Qu","given":"Chunxu"},{"affiliation":[],"family":"Jiao","given":"Yun"},{"affiliation":[],"family":"Smeyne","given":"Richard J."}],"member":"http:\\/\\/id.crossref.org\\/member\\/340","container-title":["PLoS ONE"],"deposited":{"date-parts":[[2014,3,5]],"timestamp":1393977600000},"score":1.0,"subtitle":[],"editor":[{"affiliation":[],"family":"Borlongan","given":"Cesario V."}],"issued":{"date-parts":[[2012,3,21]]},"URL":"http:\\/\\/dx.doi.org\\/10.1371\\/journal.pone.0033693","ISSN":["1932-6203"],"subject":["Agricultural and Biological Sciences(all)","Medicine(all)","Biochemistry, Genetics and Molecular Biology(all)"]}}'

def test_works():
    "Basic test of works"
    res = hb.works(query = "ecology", limit = 2)
    assert 'ok' == res.status()
    assert 'dict' == res.query().__class__.__name__
    assert 2 == res.items_per_page()

def test_works_filter():
    "Test of works with filter"
    res = hb.works(filter = {'has_full_text': True}, limit = 3)
    assert 'ok' == res.status()
    assert 'dict' == res.query().__class__.__name__
    assert 3 == res.items_per_page()

# """Tests for works"""
# import os
# import unittest
# from habanero import Habanero

# class TestWorksMethod(unittest.TestCase):

# 	def setUp(self):
# 		self.hb = Habanero()

#   def test_works_ids(self):
#     "works with ids param"
#     res = self.hb.works(ids = '10.1371/journal.pone.0033693')
#     self.assertEqual('ok', res.status())
#     # self.assertEqual(habanero.response.Response == res.__class__)

#   def test_works_query(self):
#     "works with query param"
#     res = self.hb.works(query = "ecology")
#     self.assertEqual('ok', res.status())

# if __name__ == '__main__':
#     unittest.main()
