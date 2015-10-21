"""Tests for works"""
import os
import unittest

from habanero import Habanero
hb = Habanero()

class TestWorksMethod(unittest.TestCase):

  def test_works_ids():
    "works with ids param"
    res = hb.works(ids = '10.1371/journal.pone.0033693')
    self.assertEqual('ok', res.status())
    # self.assertEqual(habanero.response.Response == res.__class__)

  def test_works_query():
    "works with query param"
    res = hb.works(query = "ecology")
    self.assertEqual('ok', res.status())
