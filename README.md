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
1. Go to https://localhost:8000/ and make a user with the _Create User_ button.

2. Log in with the user you just created. 

3. You should now be redirected to the url https://localhost:8000/polls/ and see no polls available 

4. Go to the url https://localhost:8000/polls/CreateQuestion/

5. Enter your question with the publish date and click save.

6. You should now be redirected to the url https://localhost:8000/polls/<question.id>/CreateChoice/ 

7. Create as many choices as you want. Everytime you hit "Save" that choice is added to the question.

8. When you are done adding choices, hit _Exit_ and you should be redirected to your new question.

To run tests, please have two terminals open, one that runs the
webpage, and one that runs the tests using selenium.
Use the following command to run the test for the login page:

_python manage.py runserver_

_python manage.py test loginPage_


To run tests for the polls page you need only to have one terminal open.
Use the following command in the root directory of the project:

_python manage.py test polls_


