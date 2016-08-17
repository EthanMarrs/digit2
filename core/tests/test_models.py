"""test_models.py: runs tests on the models for digit."""
import pytest
from core.models import Question, Answer
from django.test import TestCase
from django.db.utils import IntegrityError


class TestQuestion(TestCase):
    """Test the Question Model."""

    def setUp(self):
        """Create questions for testing."""
        question1 = Question(content='what is 1 + 1?',
                             explanation='This is an addition question')
        question1.save()
        answer1 = Answer(content='2', question=question1)
        answer1.save()

    def test_question_deafult_state(self):
        """Confirm that default state is Incomplete."""
        question1 = Question.objects.all()[0]
        assert(question1.state == 1)

    def test_question_answer_relation(self):
        """Confirm that question can only have one answer."""
        question1 = Question.objects.all()[0]
        with pytest.raises(IntegrityError) as exception_info:
            another_answer = Answer(content='3', question=question1)
            another_answer.save()
        assert(exception_info.value.__str__() ==
               "UNIQUE constraint failed: core_answer.question_id")

    def test_question_state_from_incomplete_to_review_ready(self):
        """Check that question state.

        Confirm that state can only go from 'incomplete' to
        'ready for review'.
        """
        question1 = Question.objects.all()[0]
        with pytest.raises(Exception) as exception_info:
            question1.change_to_needs_reworking()
        for item in dir(exception_info):
            print(item)
        assert(exception_info.value.__str__() ==
               "Incorrect state change. Current state is 1")
