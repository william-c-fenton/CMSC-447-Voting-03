from django.test import TestCase

# Create your tests here.
import unittest
from django.shortcuts import render
from django.utils import timezone

from polls.models import Question, Choice, Vote
from loginPage.models import VoterInfo

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys

from django.test import Client
from django.urls import reverse

# Tests if the pages exist and can be modified
from polls.models import Question


class URLTests(unittest.TestCase):
    # Set up a Chrome browser
    @classmethod
    def setUpClass(self):
        self.driver = webdriver.Chrome(executable_path=r'C:\chromedriver.exe')
    
    @classmethod
    def tearDownClass(self):
        self.driver.close()

    # Go to polls page to make sure user cannot get access to it
    def denyAccessTest(self):
        # Delete pre-existing user
        user = authenticate(username='Test', email='test@example.com', password='12345')
        if not (user is None):
            u = User.objects.get(username='Test', email='test@example.com', password='12345')
            u.delete()

        # Go to each poll page and see if information is missing
        driver = self.driver
        driver.get('http://127.0.0.1:8000/polls/')
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/polls/')
        self.assertTrue(driver.find_element_by_id("error"))
        self.assertTrue(driver.find_element_by_id("login"))

        driver.get('http://127.0.0.1:8000/polls/')
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/polls/CreateQuestion')
        self.assertTrue(driver.find_element_by_id("error"))
        self.assertTrue(driver.find_element_by_id("login"))

    # Find the fields for test input
    def findFields(self):
        # Login normally
        driver = self.driver
        driver.get('http://127.0.0.1:8000/')
        # Does index.html take the user to the login page?
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/login/')
        self.assertTrue(driver.find_element_by_name("first name"))
        self.assertTrue(driver.find_element_by_name("last name"))
        self.assertTrue(driver.find_element_by_name("IDNum"))
        self.assertTrue(driver.find_element_by_id("help"))
        self.assertTrue(driver.find_element_by_name("submit"))

        # Error page
        driver.get('http://127.0.0.1:8000/loginError/')
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/loginError/')
        self.assertTrue(driver.find_element_by_name("first name"))
        self.assertTrue(driver.find_element_by_name("last name"))
        self.assertTrue(driver.find_element_by_name("IDNum"))
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
        idnum = driver.find_element_by_name("IDNum")
        idnum.send_keys("12345")

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
        idnum = driver.find_element_by_name("IDNum")
        idnum.send_keys("12345")

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

    def test_user_creation_fields_exist(self):
        # Set up driver. 
        driver = self.driver
        driver.get('http://127.0.0.1:8000/')

        # Find and click the create user button.
        create_user_button = driver.find_element_by_name('createUser')
        create_user_button.click()

        # Verify that the forms exist on the main createUser page. 
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/createUser/')
        self.assertTrue(driver.find_element_by_name('first name'))
        self.assertTrue(driver.find_element_by_name('last name'))
        self.assertTrue(driver.find_element_by_name('state'))
        self.assertTrue(driver.find_element_by_name('IDNum'))
        self.assertTrue(driver.find_element_by_name('email'))

        # Verify that the forms exist on the createUserError page. 
        driver.get('http://127.0.0.1:8000/createUserError/')

        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/createUserError/')
        self.assertTrue(driver.find_element_by_id('errorText'))
        self.assertTrue(driver.find_element_by_name('first name'))
        self.assertTrue(driver.find_element_by_name('last name'))
        self.assertTrue(driver.find_element_by_name('state'))
        self.assertTrue(driver.find_element_by_name('IDNum'))
        self.assertTrue(driver.find_element_by_name('email'))

    def test_valid_user_creation(self):
        # This test should successfully add a user into the database, 
        # and then login to make sure that the website works with the new user. 

        # First, check the database for any duplicate entries that may be left over.
        voterinfo = VoterInfo.objects.filter(
            firstName__iexact='Test',
            lastName__iexact='Guy',
            state__iexact='MD',
            IDNum__exact='12345',
            email__iexact='test@example.com'
        )
        if voterinfo:
            voterinfo.delete()

        # Delete pre-existing user
        user = authenticate(username='Test', email='test@example.com', password='12345')
        if not (user is None):
            u = User.objects.get(username='Test')
            u.delete()

        # Set up driver. 
        driver = self.driver
        driver.get('http://127.0.0.1:8000/')

        # Find and click the create user button.
        create_user_button = driver.find_element_by_name('createUser')
        create_user_button.click()

        # Verify the correct page is reached. 
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/createUser/')
        
        # Fill out the fields with test information.
        first_name_field = driver.find_element_by_name('first name')
        first_name_field.send_keys('Test')
        last_name_field = driver.find_element_by_name('last name')
        last_name_field.send_keys('Guy')
        state_field = driver.find_element_by_name('state')
        state_field.send_keys('MD')
        idnum_field = driver.find_element_by_name('IDNum')
        idnum_field.send_keys('12345')
        email_field = driver.find_element_by_name('email')
        email_field.send_keys('test@example.com')

        # Click the sign up button.
        driver.find_element_by_name('submit').click()

        # Check user
        user = authenticate(username='Test', email='test@example.com', password='12345')
        self.assertTrue(not (user is None))

        # This should pass, so we should be on the login page now. 
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/login/')

        # If the user was correctly added, we should be able to log in and go to the polls page. 
        first_name_field = driver.find_element_by_name('first name')
        first_name_field.send_keys('Test')

        last_name_field = driver.find_element_by_name('last name')
        last_name_field.send_keys('Guy')

        idnum_field = driver.find_element_by_name('IDNum')
        idnum_field.send_keys('12345')

        driver.find_element_by_name('submit').click()

        # Now we should be on the polls page. 
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/polls/')

        # Did we sign in properly?
        try:
            driver.find_element_by_id("error")
            self.assertTrue(False)
        except:
            self.assertTrue(True)

        # Delete the test user.
        VoterInfo.objects.filter(IDNum='12345').delete()

        # Delete django test user
        u = User.objects.get(username='Test')
        u.delete()

    def test_failing_user_creation(self):
        # This test should fail to add a user to the database, 
        # and take us to the createUserError page. 

        # Create test user.
        voterinfo = VoterInfo(
            firstName='Test',
            lastName='Guy',
            state='MD',
            IDNum='12345',
            email='test@example.com'
        )

        voterinfo.save()

        # Set up driver. 
        driver = self.driver
        driver.get('http://127.0.0.1:8000/')

        # Find and click the create user button.
        create_user_button = driver.find_element_by_name('createUser')
        create_user_button.click()

        # Verify the correct page is reached. 
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/createUser/')
        
        # Fill out the fields with test information.
        first_name_field = driver.find_element_by_name('first name')
        first_name_field.send_keys('Test')
        last_name_field = driver.find_element_by_name('last name')
        last_name_field.send_keys('Guy')
        state_field = driver.find_element_by_name('state')
        state_field.send_keys('MD')
        idnum_field = driver.find_element_by_name('IDNum')
        idnum_field.send_keys('12345')
        email_field = driver.find_element_by_name('email')
        email_field.send_keys('test@example.com')

        # Click the sign up button.
        driver.find_element_by_name('submit').click()

        # This should fail, so we should be on createUserError page. 
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/createUserError/')
        
        # Delete the test user. 
        VoterInfo.objects.filter(
            firstName__iexact='Test',
            lastName__iexact='Guy',
            state__iexact='MD',
            IDNum__exact='12345',
            email__iexact='test@example.com'
        ).delete()


        

