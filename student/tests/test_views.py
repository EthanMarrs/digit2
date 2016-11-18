from core.models import (Grade,
                         Subject,
                         Question,
                         Option,
                         Topic,
                         Class,
                         Block,
                         Syllabus
                         )
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime;


class StaticPageViewTests(TestCase):
    """
    Tests for all the static pages of the app.
    Includes home page and others.
    """

    def test_get_home_page(self):
        """
        Test that the home page loads correctly.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to Dig-it")
        self.assertTemplateUsed(response, 'home.html')


class QuestionViewTests(TestCase):
    """
    Tests for all question related views.
    Important to test correct delivery of questions.
    """
    def setUp(self):
        user = User.objects.create_user('temp', 'temporary@temp.com', 'temporary')
        grade_test = Grade.objects.create(name="Grade Example")
        syllabus_test = Syllabus.objects.create(grade=grade_test)
        class_test = Class.objects.create(name="Test Class",
                                          syllabus=syllabus_test)
        class_test.users.add(user)
        class_test.save()
        topic_test = Topic.objects.create(name="Financial Mathematics",
                                          description="Topic that involves sinking funds "
                                          "and loan calculations",
                                          syllabus=syllabus_test,
                                          week_start=int(datetime.now().strftime("%V")),
                                          duration=3)

    def test_get_quiz(self):
        """
        Test for the main quiz view.
        Probably the most complex view in the app, important tests.
        """
        # Make sure there is a question to serve
        question = Question.objects.first()
        question.live = True
        question.content = "Test question"
        question.save()

        self.client.login(username='temp', password='temporary')
        response = self.client.get('/quiz/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz.html')
        self.assertQuerysetEqual(
            [response.context['question']],
            ['<Question: Question ' + str(question.uuid)[0:8] + '>']
        )

    def test_get_quiz_empty_question_pool(self):
        """
        Test for the main quiz view.
        Checks student does not get question
        """
        self.client.login(username='temp', password='temporary')
        response = self.client.get('/quiz/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz.html')
        self.assertQuerysetEqual(
            [response.context['question']],
            ['None']
        )
        self.assertContains(response, "You have completed all questions in the available pool.")


class SignupViewTests(TestCase):
    """
    Tests for student signup on the platform.
    """

    def test_get_signup(self):
        """
        Test that the home page loads correctly.
        """
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Signup")
        self.assertTemplateUsed(response, 'signup.html')

    def test_post_signup(self):
        """
        Test student signup form works correctly.
        """
        data = {"username": "tester",
                "first_name": "Test",
                "last_name": "User",
                "email": "test@test.com",
                "password": "testing12"}
        response = self.client.post('/signup/', data=data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, "tester")
        self.assertRedirects(response, '/welcome/', status_code=302)
