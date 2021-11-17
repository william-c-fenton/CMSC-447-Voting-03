from django.test import TestCase

# Create your tests here.
import unittest
from django.shortcuts import render

# Tests if the pages exist
class URLTests(unittest.TestCase):
    # Can the login page be loaded?
    def testGetLoginPage(self):
        request = 'index'
        self.assertTrue(render(request, 'adminPage/index.html', context={}))