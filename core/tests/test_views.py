"""test_views.py: runs tests on the views for digit."""
import pytest
from core.models import (Grade,
                         Subject,
                         Question,
                         Comment,
                         Option,
                         Topic,
                         Block,
                         Syllabus,
                         QuestionOrder,
                         StateException,
                         CorrectOptionExistsError,
                         )
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
import json


class BlockViewTests(TestCase):
    """
    Test all Block views.
    """
    def setUp(self):
        user = User.objects.create_user('temp', 'temporary@temp.com', 'temporary')
        grade_test = Grade.objects.create(name="Grade Example")
        syllabus_test = Syllabus.objects.create(grade=grade_test)
        Topic.objects.create(name="Financial Mathematics",
                             description="Topic that involves sinking funds "
                                         "and loan calculations",
                             syllabus=syllabus_test, week_start=1,
                             duration=3)

    def test_get_blocks(self):
        """
        Test that blocks are listed.
        """
        self.client.login(username='temp', password='temporary')
        response = self.client.get('/blocks/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Financial Mathematics")
        self.assertQuerysetEqual(
            [response.context['object']],
            ['<Block: Financial Mathematics Block 1>']
        )

    def test_post_block_update(self):
        """
        Test updating block description.
        """
        self.client.login(username='temp', password='temporary')
        data = {"text": "yep!"}
        response = self.client.post('/blocks/1/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Block.objects.first().description, "yep!")


class QuestionOrderTests(TestCase):
    """
    Test all Question Order views.
    """
    def setUp(self):
        user = User.objects.create_user('temp', 'temporary@temp.com', 'temporary')
        creator = User.objects.create_user('creator', 'creator@creator.com', 'creator')
        moderator = User.objects.create_user('moderator', 'moderator@moderator.com', 'moderator')
        grade_test = Grade.objects.create(name="Grade Example")
        syllabus_test = Syllabus.objects.create(grade=grade_test)
        topic = Topic.objects.create(name="Financial Mathematics",
                                     description="Topic that involves sinking funds "
                                                 "and loan calculations",
                                     syllabus=syllabus_test, week_start=1,
                                     duration=3)
        QuestionOrder.objects.create(assigned_to=creator,
                                     assigned_by=user,
                                     moderator=moderator,
                                     topic=topic,
                                     description="Create some financial math questions please.",
                                     due_date=date.today()+timedelta(days=30))

    def test_get_question_order(self):
        """
        Test that question order is displayed.
        """
        self.client.login(username='temp', password='temporary')
        response = self.client.get('/question_orders/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'question_order.html')
        self.assertContains(response, "Financial Mathematics")
        self.assertIn(b"Create some financial math questions please.", response.content)
        self.assertQuerysetEqual(
            [response.context['object']],
            ['<QuestionOrder: Financial Mathematics Question Order>']
        )

    def test_get_question_orders(self):
        """
        Test that question orders list is displayed.
        """
        self.client.login(username='temp', password='temporary')
        response = self.client.get('/question_orders/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'question_orders.html')
        self.assertIn(b"Financial Mathematics", response.content)
        self.assertQuerysetEqual(
            [response.context['object_list']],
            ['<QuerySet [<QuestionOrder: Financial Mathematics Question Order>]>']
        )

    def test_post_question_order_live(self):
        """
        Test that question order's questions are live when the endpoint is hit.
        """
        self.client.login(username='temp', password='temporary')
        response = self.client.post('/question_orders/1/live/')
        self.assertEqual(response.status_code, 200)
        block = Block.objects.filter(topic_id=1).first()
        question = block.get_questions().first()
        self.assertTrue(question.live)

    def test_post_question_order_open(self):
        """
        Test that question order is open when the endpoint is hit.
        """
        data = {"state": "true"}
        self.client.login(username='temp', password='temporary')
        response = self.client.post('/question_orders/1/open/', data=data)
        self.assertEqual(response.status_code, 200)
        order = QuestionOrder.objects.first()
        self.assertTrue(order.open)


class TopicViewTests(TestCase):
    """
    Test all topic views.
    """
    def setUp(self):
        user = User.objects.create_user('temp', 'temporary@temp.com', 'temporary')
        grade_test = Grade.objects.create(name="Grade Example")
        self.syllabus_test = Syllabus.objects.create(grade=grade_test)

    def test_get_topic_create_wizard(self):
        """
        Test that the form for the topic creation wizard is rendered correctly.
        """
        self.client.login(username='temp', password='temporary')
        response = self.client.get('/topic_create_wizard/')
        self.assertTemplateUsed(response, 'topic_create_wizard.html')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Year Overview", response.content)

    def test_post_topic_create_wizard(self):
        """
        Test that posting a new topic using the creation wizard works correctly.
        """
        self.client.login(username='temp', password='temporary')
        data = {"syllabus": "1",
                "name": "Test",
                "description": "Testing",
                "week_start": "1",
                "duration": "4"}
        response = self.client.post('/topic_create_wizard/', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Topic.objects.all().count(), 1)


class SyllabusViewTests(TestCase):
    """
    Test important syllabus views.
    """
    def setUp(self):
        user = User.objects.create_user('temp', 'temporary@temp.com', 'temporary')
        grade_test = Grade.objects.create(name="Grade Example")
        self.syllabus_test = Syllabus.objects.create(grade=grade_test)
        topic = Topic.objects.create(name="Financial Mathematics",
                                     description="Topic that involves sinking funds "
                                                 "and loan calculations",
                                     syllabus=self.syllabus_test, week_start=1,
                                     duration=3)

    def test_get_syllabi(self):
        """
        Test that syllabi are listed correctly.
        """
        self.client.login(username='temp', password='temporary')
        response = self.client.get('/syllabi/')
        self.assertTemplateUsed(response, 'syllabi.html')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Syllabus List", response.content)
        self.assertIn(b"Grade Example", response.content)

    def test_get_syllabus_timeline(self):
        """
        Test the syllabus timeline view. This has fairly complex visual elements.
        """
        self.client.login(username='temp', password='temporary')
        response = self.client.get('/syllabi/1/timeline/')
        self.assertTemplateUsed(response, 'timeline.html')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Financial Mathematics", response.content)
        self.assertIn(b"Grade Example Syllabus", response.content)
        self.assertIn("Topic that involves sinking funds", str(response.context['data']))
        self.assertIn("'number_of_blocks': 3", str(response.context['data']))


class QuestionContentViewTest(TestCase):
    """
    Test content is created properly using content view.
    """
    def setup(self):
        pass

    def test_simple_question_update(self):
        """
        Pass in a simple JSON file.
        """
        question_id = 123
        Question(id=question_id).save()

        user = User.objects.create(username='testuser')
        user.set_password('password')
        user.save()

        self.client = Client()
        logged_in = self.client.login(username='testuser', password='password')

        assert(logged_in)

        data = {
            "name": question_id,
            "question_content": [
                {"text": "This is a test question", "inline": False},
            ],
            "option_content_1": [
                {"text": "option 1", "inline": False}
            ],
            "option_content_2": [
                {"text": "option 2", "inline": False}
            ],
            "option_content_3": [
                {"text": "option 3", "inline": False}
            ],
            "additional_information": [],
            "answer_explanation_content": [
                {"text": "This is the answer", "inline": False},
            ]
        }

        response = self.client.post('/question_content/',
                                    json.dumps(data),
                                    content_type="application/json")
        assert(response.status_code == 200)
        question = Question.objects.get(id=123)
        assert(question.question_content == "<p>This is a test question</p>")
        assert(question.answer_content == "<p>This is the answer</p>")
        # fetch the associated options
        options = Option.objects.filter(question=question)
        # assumes questions are created in the order that is created
        assert(len(options) == 3)
        assert(options[0].content == "<p>option 1</p>")
        assert(options[1].content == "<p>option 2</p>")
        assert(options[2].content == "<p>option 3</p>")

        new_data = {
            "name": question_id,
            "question_content": [
                {"text": "new question text", "inline": False},
            ],
            "option_content_1": [
                {"text": "new option 1", "inline": False}
            ],
            "option_content_2": [
                {"text": "new option 2", "inline": False}
            ],
            "option_content_3": [
                {"text": "new option 3", "inline": False}
            ],
            "additional_information": [],
            "answer_explanation_content": [
                {"text": "new answer text", "inline": False},
            ]
        }

        response = self.client.post('/question_content/',
                                    json.dumps(new_data),
                                    content_type="application/json")
        assert(response.status_code == 200)
        question = Question.objects.get(id=123)
        assert(question.question_content == "<p>new question text</p>")
        assert(question.answer_content == "<p>new answer text</p>")
        # fetch the associated options
        options = Option.objects.filter(question=question)
        # assumes questions are created in the order that is created
        assert(len(options) == 3)
        assert(options[0].content == "<p>new option 1</p>")
        assert(options[1].content == "<p>new option 2</p>")
        assert(options[2].content == "<p>new option 3</p>")
