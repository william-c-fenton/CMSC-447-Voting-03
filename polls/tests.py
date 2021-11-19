from django.test import TestCase, Client, LiveServerTestCase
from django.utils import timezone
from django.urls import reverse, path
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Question, Choice, Vote
from loginPage.models import VoterInfo

from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from time import sleep

# class QuestionModelTests(TestCase):
#
#     def test_was_published_recently_with_future_question(self):
#         """
#         was_published_recently() returns False for questions whose pub_date
#         is in the future.
#         """
#         time = timezone.now() + datetime.timedelta(days=30)
#         future_question = Question(pub_date=time)
#         self.assertIs(future_question.was_published_recently(), False)
#
#     def test_was_published_recently_with_old_question(self):
#         """
#         was_published_recently() returns False for questions whose pub_date
#         is older than 1 day.
#         """
#         time = timezone.now() - datetime.timedelta(days=1, seconds=1)
#         old_question = Question(pub_date=time)
#         self.assertIs(old_question.was_published_recently(), False)
#
#     def test_was_published_recently_with_recent_question(self):
#         """
#         was_published_recently() returns True for questions whose pub_date
#         is within the last day.
#         """
#         time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
#         recent_question = Question(pub_date=time)
#         self.assertIs(recent_question.was_published_recently(), True)
#
# def create_question(question_text, days):
#     """
#     Create a question with the given `question_text` and published the
#     given number of `days` offset to now (negative for questions published
#     in the past, positive for questions that have yet to be published).
#     """
#     time = timezone.now() + datetime.timedelta(days=days)
#     return Question.objects.create(question_text=question_text, pub_date=time)
#
#
# class QuestionIndexViewTests(TestCase):
#     def test_no_questions(self):
#         """
#         If no questions exist, an appropriate message is displayed.
#         """
#         response = self.client.get(reverse('polls:index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])
#
#     def test_past_question(self):
#         """
#         Questions with a pub_date in the past are displayed on the
#         index page.
#         """
#         question = create_question(question_text="Past question.", days=-30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             [question],
#         )
#
#     def test_future_question(self):
#         """
#         Questions with a pub_date in the future aren't displayed on
#         the index page.
#         """
#         create_question(question_text="Future question.", days=30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])
#
#     def test_future_question_and_past_question(self):
#         """
#         Even if both past and future questions exist, only past questions
#         are displayed.
#         """
#         question = create_question(question_text="Past question.", days=-30)
#         create_question(question_text="Future question.", days=30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             [question],
#         )
#
#     def test_two_past_questions(self):
#         """
#         The questions index page may display multiple questions.
#         """
#         question1 = create_question(question_text="Past question 1.", days=-30)
#         question2 = create_question(question_text="Past question 2.", days=-5)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             [question2, question1],
#         )
#
# class QuestionDetailViewTests(TestCase):
#     def test_future_question(self):
#         """
#         The detail view of a question with a pub_date in the future
#         returns a 404 not found.
#         """
#         future_question = create_question(question_text='Future question.', days=5)
#         url = reverse('polls:detail', args=(future_question.id,))
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 404)
#
#     def test_past_question(self):
#         """
#         The detail view of a question with a pub_date in the past
#         displays the question's text.
#         """
#         past_question = create_question(question_text='Past Question.', days=-5)
#         url = reverse('polls:detail', args=(past_question.id,))
#         response = self.client.get(url)
#         self.assertContains(response, past_question.question_text)
#
# class ResultsViewTests(TestCase):
#     @classmethod
#     def setUpClass(self):
#         self.driver = webdriver.Chrome(executable_path='C:\chromedriver.exe')
#
#         self.question = Question.objects.create(question_text='Does this work?', pub_date=timezone.now())
#
#         self.question.choice_set.create(choice_text='Yes')
#         self.question.choice_set.create(choice_text='No')
#
#     @classmethod
#     def tearDownClass(self):
#         self.driver.close()
#
#     def test_vote_takes_user_to_results_page(self):
#         # Verify that the webpage takes you to the results page after clicking the vote button.
#
#         # Navigate to the voting page for our poll.
#         driver = self.driver
#         driver.get(f'http://127.0.0.1:8000/polls/{self.question.id}')
#
#         # Input a vote (just the first option is fine here).
#         driver.find_element_by_id('choice1').click()
#
#         # Select the "Vote" button, which should add a vote to the database and take us to the results page.
#         driver.find_element_by_xpath(".//input[@value='Vote']").click()
#
#         # Verify that we are now currently on the results page.
#         self.assertEqual(driver.current_url,
#             f'http://127.0.0.1:8000/polls/{self.question.id}/results/')


class BallotCreationTests(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.driver = webdriver.Chrome(executable_path='C:\chromedriver.exe')

        self.question = Question.objects.create(question_text='Does this work?', pub_date=timezone.now())

        self.question.choice_set.create(choice_text='Yes')
        self.question.choice_set.create(choice_text='No')
        super().setUpClass()

    @classmethod
    def tearDownClass(self):
        self.driver.close()
        super().tearDownClass()

    # helper method to open to a specific page
    def open(self, extension):
        self.driver.get("%s%s" % (self.live_server_url, extension))

    # helper method to get current url with extensions
    def get_url(self, extension):
        return "%s%s" % (self.live_server_url, extension)

    # helper method to login and create dummy user
    def dummy_login(self):
        info = VoterInfo(firstName="Test", lastName="Guy", state="MD", IDNum="12345", email="test@example.com", )
        info.save()

        # Make user
        user = User.objects.create_user(username="Test", email="test@example.com", password="12345")
        user.save()

        # Login normally
        driver = self.driver
        self.open('/login/')

        first = driver.find_element_by_name("first name")
        first.send_keys("Test")
        last = driver.find_element_by_name("last name")
        last.send_keys("Guy")
        idnum = driver.find_element_by_name("IDNum")
        idnum.send_keys("12345")
        submit = driver.find_element_by_name("submit")
        submit.click()

    def test_login_to_index(self):
        # Verify that the webpage takes you to the index page after logging in

        # Add test voter information
        info = VoterInfo(firstName="Test", lastName="Guy", state="MD", IDNum="12345", email="test@example.com", )
        info.save()

        # Make user
        user = User.objects.create_user(username="Test", email="test@example.com", password="12345")
        user.save()

        # Login normally
        driver = self.driver
        self.open('/login/')

        self.assertEqual(driver.current_url, self.get_url('/login/'))
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
        self.assertEqual(driver.current_url, self.get_url('/polls/'))

    def test_question_creation(self):
        # Verify that a question added through the ballot creation page is in the database

        question_string = "What is up?"
        now_string = datetime.now().strftime("%Y-%m-%d")

        # Go to the ballot creation page
        self.dummy_login()
        self.open('/polls/CreateQuestion/')
        self.assertEqual(self.driver.current_url, self.get_url('/polls/CreateQuestion/'))

        # Create the question as normal
        question_text = self.driver.find_element_by_name("question_text")
        question_text.send_keys(question_string)
        pub_date = self.driver.find_element_by_name("pub_date")
        pub_date.send_keys(now_string)
        submit = self.driver.find_element_by_name("submit")
        submit.click()

        # Verify that our new question is in the database
        self.assertTrue(Question.objects.filter(question_text=question_string).exists())

    def test_question_creation_to_choice_creation(self):
        # Verify that you are taken to the choice creation page after creating a question

        question_string = "What is up dog?"
        now_string = datetime.now().strftime("%Y-%m-%d")

        # Go to the ballot creation page
        self.dummy_login()
        self.open('/polls/CreateQuestion/')
        self.assertEqual(self.driver.current_url, self.get_url('/polls/CreateQuestion/'))

        # Create the question as normal
        question_text = self.driver.find_element_by_name("question_text")
        question_text.send_keys(question_string)
        pub_date = self.driver.find_element_by_name("pub_date")
        pub_date.send_keys(now_string)
        submit = self.driver.find_element_by_name("submit")
        submit.click()

        new_question = Question.objects.get(question_text=question_string)
        # Verify that we were sent to the choice creation page
        self.assertEqual(self.driver.current_url, self.get_url('/polls/' + str(new_question.id) + '/CreateChoice/'))

    def test_choice_creation(self):
        # Verify that a choice added through the choice creation page is added to the correct question

        question_string = "What is up my homie?"
        now_string = datetime.now().strftime("%Y-%m-%d")

        # Go to the ballot creation page
        self.dummy_login()
        self.open('/polls/CreateQuestion/')
        self.assertEqual(self.driver.current_url, self.get_url('/polls/CreateQuestion/'))

        # Create the question as normal
        question_text = self.driver.find_element_by_name("question_text")
        question_text.send_keys(question_string)
        pub_date = self.driver.find_element_by_name("pub_date")
        pub_date.send_keys(now_string)
        submit = self.driver.find_element_by_name("submit")
        submit.click()

        new_question = Question.objects.get(question_text=question_string)
        # Verify that we were sent to the choice creation page
        self.assertEqual(self.driver.current_url, self.get_url('/polls/' + str(new_question.id) + '/CreateChoice/'))

        # Create the choices as normal
        choice_text = self.driver.find_element_by_name("choice_text")
        choice_text.send_keys("Not much, boss.")
        submit = self.driver.find_element_by_name("savebtn")
        submit.click()

        choice_text = self.driver.find_element_by_name("choice_text")
        choice_text.send_keys("The sky, I think.")
        submit = self.driver.find_element_by_name("savebtn")
        submit.click()

        exit_btn = self.driver.find_element_by_name("exitbtn")
        exit_btn.click()

        # Verify that our new choices are associated with our new question
        self.assertTrue(Choice.objects.filter(choice_text="Not much, boss.", question=new_question).exists())
        self.assertTrue(Choice.objects.filter(choice_text="The sky, I think.", question=new_question).exists())

    def test_choice_creation_to_question_detail(self):
        # Verify that you are taken to the question detail page after creating a choice and hitting "Exit" button

        question_string = "What is up my driller?"
        now_string = datetime.now().strftime("%Y-%m-%d")

        # Go to the ballot creation page
        self.dummy_login()
        self.open('/polls/CreateQuestion/')
        self.assertEqual(self.driver.current_url, self.get_url('/polls/CreateQuestion/'))

        # Create the question as normal
        question_text = self.driver.find_element_by_name("question_text")
        question_text.send_keys(question_string)
        pub_date = self.driver.find_element_by_name("pub_date")
        pub_date.send_keys(now_string)
        submit = self.driver.find_element_by_name("submit")
        submit.click()

        new_question = Question.objects.get(question_text=question_string)
        # Verify that we were sent to the choice creation page
        self.assertEqual(self.driver.current_url, self.get_url('/polls/' + str(new_question.id) + '/CreateChoice/'))

        # Create the choices as normal
        choice_text = self.driver.find_element_by_name("choice_text")
        choice_text.send_keys("Not much.")
        submit = self.driver.find_element_by_name("savebtn")
        submit.click()

        choice_text = self.driver.find_element_by_name("choice_text")
        choice_text.send_keys("The sky.")
        submit = self.driver.find_element_by_name("savebtn")
        submit.click()

        exit_btn = self.driver.find_element_by_name("exitbtn")
        exit_btn.click()

        # Verify that we were sent to the correct question detail page
        self.assertEqual(self.driver.current_url, self.get_url('/polls/' + str(new_question.id) + '/'))
