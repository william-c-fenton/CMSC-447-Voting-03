# CMSC-447-Voting-03
Secure voting project for CMSC 447 with Ben Johnson. 

#Setup:

Please be sure to have the software installed as outlined
in requirements.txt, especially Python 3 and Django ver. 3.2.8!

The webpage was developed and run in PyCharm 2021.2.2 Professional
Edition. Execution instructions are as follows:

#Execution of program:

Use the following command to run the webpage.
Click the link provided to be taken to the webpage:

_python manage.py runserver_

Do the following to create a question and view it:
1. Create an admin user with the following command:
_python manage.py createsuperuser_

2. Go to https://localhost:8000/admin/ and login as the admin you just created.

3. Click on the Questions page in Django admin under Polls and add a Question and then save it

4. Next open up the Django shell with the command: _python manage.py shell_

5. Enter the following in the shell 
>>> from polls.models import Choice, Question
>>> q = Question.objects.get(pk=1)
>>> q.choice_set.create(choice_text='Yes', votes=0)
>>> q.choice_set.create(choice_text='No', votes=0)
>>> exit()

6. The poll should now show up under the page https://localhost:8000/polls/

7. Click on the question and vote on it.


Use the following command to run the test for the login page:

_python manage.py test loginPage_

Use the following command to run the tests for the polls voting page:

_python manage.py test polls_

#Using the program:

At the moment, there are no features provided on the
webpage.

At the moment, these are rather unorganized Django apps, and in the future they will be more coherent. 
