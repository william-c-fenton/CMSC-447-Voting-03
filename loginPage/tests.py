from django.test import TestCase

# Create your tests here.
import unittest
from django.shortcuts import render
from django.utils import timezone

from polls.models import Question, Choice, Vote
from loginPage.models import VoterInfo

from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys

from django.test import Client
from django.urls import reverse

# Tests if the pages exist and can be modified
from polls.models import Question


class URLTests(unittest.TestCase):
    # Set up a Chrome browser
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=r'C:\chromedriver.exe')

    # Find the fields for test input
    def findFields(self):
        # Login normally
        driver = self.driver
        driver.get('http://127.0.0.1:8000/')
        # Does index.html take the user to the login page?
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/login/')
        self.assertTrue(driver.find_element_by_name("first name"))
        self.assertTrue(driver.find_element_by_name("last name"))
        self.assertTrue(driver.find_element_by_name("state"))
        self.assertTrue(driver.find_element_by_name("IDNum"))
        self.assertTrue(driver.find_element_by_name("email"))
        self.assertTrue(driver.find_element_by_id("help"))
        self.assertTrue(driver.find_element_by_name("submit"))

        # Error page
        driver.get('http://127.0.0.1:8000/loginError/')
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/loginError/')
        self.assertTrue(driver.find_element_by_name("first name"))
        self.assertTrue(driver.find_element_by_name("last name"))
        self.assertTrue(driver.find_element_by_name("state"))
        self.assertTrue(driver.find_element_by_name("IDNum"))
        self.assertTrue(driver.find_element_by_name("email"))
        self.assertTrue(driver.find_element_by_id("help"))
        self.assertTrue(driver.find_element_by_name("submit"))

        # Help page
        driver.get('http://127.0.0.1:8000/loginHelp/')
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/loginHelp/')
        self.assertTrue(driver.find_element_by_id("back"))

    # Can the fields have data entered into them?
    # Can the login info take the user to the polls page?
    def testFieldInputTrue(self):
        # Add test voter information
        info = VoterInfo(firstName="Test", lastName="Guy", state="Maryland", IDNum="12345", email="123@email.com",)
        info.save()

        # Login normally
        driver = self.driver
        driver.get('http://127.0.0.1:8000/')
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/login/')
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

        # Was login successful?
        # NOTE: was edited to polls page
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/polls/')

        # Go back to login page, then test if the incorrect input takes user to error page.
        driver.get('http://127.0.0.1:8000/')
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/login/')

        submit = driver.find_element_by_name("submit")
        submit.click()

        # Did login fail?
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

        # Was login successful?
        # NOTE: was edited to polls page
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/polls/')

        # Delete test voter information
        VoterInfo.objects.filter(IDNum='12345').delete()

    # Can the user get to the help page?
    def testHelp(self):
        # Go to login page
        driver = self.driver
        driver.get('http://127.0.0.1:8000/')

        helplink = driver.find_element_by_id("help")
        helplink.click()

        # Did the link take the user to the help page?
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/loginHelp/')

        # Go back to login page, by pressing back link.
        back = driver.find_element_by_id("back")
        back.click()
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/login/')

        # Go to error page, and try help link there
        submit = driver.find_element_by_name("submit")
        submit.click()

        # Did login fail?
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/loginError/')

        helplink = driver.find_element_by_id("help")
        helplink.click()

        # Did the link take the user to the help page?
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/loginHelp/')

        # Go back to login page, by pressing back link.
        back = driver.find_element_by_id("back")
        back.click()
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/login/')

    # Close the Chrome browser
    def tearDown(self):
        self.driver.close()
