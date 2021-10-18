from django.test import TestCase

# Create your tests here.
import unittest
from django.shortcuts import render

#Tests if the pages exist
class URLTests(unittest.TestCase):
    def testGetLoginPage(self):
        request = 'index'
        self.assertTrue(render(request, 'loginPage/index.html', context={}))