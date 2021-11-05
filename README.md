# CMSC-447-Voting-03
Secure voting project for CMSC 447 with Ben Johnson. 

#Setup:

This program REQUIRES python 3.9.7 (as opposed to 3.10.0, not sure if it works on other versions/patches).

Please be sure to have the software installed as outlined in requirements.txt. If you're using the correct version of Python, everything should install smoothly.

To use the selenium tests, please use a Chrome webdriver, and keep it in the C:\ drive.

The webpage was developed and run in PyCharm 2021.2.2 Professional Edition. Execution instructions are as follows:

#Execution of program:

Use the following commands to run the webpage.
Click the link provided to be taken to the webpage:

_python manage.py runserver_

Do the following to create a question and view it:
1. Create an admin user with the following command:
_python manage.py createsuperuser_

2. Go to https://localhost:8000/admin/ and login as the admin you just created.

3. Click on the Questions page in Django admin under Polls and add a Question and then save it

4. Next open up the Django shell with the command: _python manage.py shell_

5. Enter the following in the shell 
- from polls.models import Choice, Question
- q = Question.objects.get(pk=1)
- q.choice_set.create(choice_text='Yes', votes=0)
- q.choice_set.create(choice_text='No', votes=0)
- exit()

6. The poll should now show up under the page https://localhost:8000/polls/

7. Click on the question and vote on it.

To run tests, please have two terminals open, one that runs the
webpage, and one that runs the tests using selenium.
Use the following command to run the test for the login page:

_python manage.py runserver_

_python manage.py test loginPage_

or, 

_python manage.py test polls_

#Using the program:

At the moment, there are no features provided on the
webpage.

At the moment, these are rather unorganized Django apps, and in the future they will be more coherent. 
