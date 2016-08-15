from core.models import Question, Answer
from django.test import TestCase


class TestQuestion(TestCase):
    def setUp(self):
        question = Question(content='What is the airspeed velocity of an unladen swallow?',
                            explanation='Invert the midpoint Strouhal number (which is 0.3). This means that the \
                            airspeed about 3 times the product of the frequency and the amplitude.')
        answer = Answer(content='11 meters per second.', question=question)

    def test_test(self):
        assert(True)