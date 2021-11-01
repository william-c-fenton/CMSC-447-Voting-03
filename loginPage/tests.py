from django.test import TestCase

# Create your tests here.
import unittest
from django.shortcuts import render
from loginPage.models import VoterInfo

from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys

from django.test import Client

# Tests if the pages exist and can be modified
class URLTests(unittest.TestCase):
    # -This test no longer can function due to the inclusion of the csrf_token.
    # Can the login page be loaded?
    # def testGetLoginPage(self):
    #     request = 'login'
    #     voterinfo = VoterInfo.objects.filter()
    #     context = {
    #         'voterinfo': voterinfo
    #     }
    #     self.assertTrue(render(request, 'loginPage/login.html', context={}))

    # Set up a Chrome browser
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=r'C:\chromedriver.exe')

    # Find the fields for test input
    def findFields(self):
        # Login normally
        driver = self.driver
        self.assertTrue(driver.get("http://127.0.0.1:8000/login"))
        self.assertTrue(driver.find_element_by_name("first name"))
        self.assertTrue(driver.find_element_by_name("last name"))
        self.assertTrue(driver.find_element_by_name("state"))
        self.assertTrue(driver.find_element_by_name("IDNum"))
        self.assertTrue(driver.find_element_by_name("email"))
        self.assertTrue(driver.find_element_by_name("help"))
        self.assertTrue(driver.find_element_by_name("submit"))

        # Error page
        self.assertTrue(driver.get("http://127.0.0.1:8000/loginError"))
        self.assertTrue(driver.find_element_by_name("first name"))
        self.assertTrue(driver.find_element_by_name("last name"))
        self.assertTrue(driver.find_element_by_name("state"))
        self.assertTrue(driver.find_element_by_name("IDNum"))
        self.assertTrue(driver.find_element_by_name("email"))
        self.assertTrue(driver.find_element_by_name("help"))
        self.assertTrue(driver.find_element_by_name("submit"))

    # Can the fields have data entered into them?
    # Can the login info take the user to the success page?
    def testFieldInputTrue(self):
        # Add test voter information
        info = VoterInfo(firstName="Test", lastName="Guy", state="Maryland", IDNum="12345", email="123@email.com",)
        info.save()

        # Login normally
        driver = self.driver
        driver.get("http://127.0.0.1:8000/login")
        first = driver.find_element_by_name("first name")
        first.send_keys("Test")
        last = driver.find_element_by_name("last name")
        last.send_keys("Guy")
        state = driver.find_element_by_name("state")
        state.send_keys("Maryland")
        idnum = driver.find_element_by_name("IDNum")
        idnum.send_keys("12345")
        email = driver.find_element_by_name("email")
        email.send_keys("123@email.com")

        submit = driver.find_element_by_name("submit")
        submit.click()

        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/loginSuccess/')

        # Go back to login page, then test if the incorrect input takes user to error page.
        driver.get("http://127.0.0.1:8000/login")

        submit = driver.find_element_by_name("submit")
        submit.click()

        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/loginError/')

        # Do login steps again
        first = driver.find_element_by_name("first name")
        first.send_keys("Test")
        last = driver.find_element_by_name("last name")
        last.send_keys("Guy")
        state = driver.find_element_by_name("state")
        state.send_keys("Maryland")
        idnum = driver.find_element_by_name("IDNum")
        idnum.send_keys("12345")
        email = driver.find_element_by_name("email")
        email.send_keys("123@email.com")

        submit = driver.find_element_by_name("submit")
        submit.click()

        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/loginSuccess/')

        # Delete test voter information
        VoterInfo.objects.filter(IDNum='12345').delete()

    # Close the Chrome browser
    def tearDown(self):
        self.driver.close()
