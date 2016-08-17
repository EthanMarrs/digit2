"""test_models.py: runs tests on the models for digit."""
import pytest
from core.models import Question, Answer, StateException
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
        assert(question1.state == question1.INCOMPLETE)

    def test_question_answer_relation(self):
        """Confirm that question can only have one answer."""
        question1 = Question.objects.all()[0]
        with pytest.raises(IntegrityError) as exception_info:
            another_answer = Answer(content='3', question=question1)
            another_answer.save()
        assert(exception_info.value.__str__() ==
               "UNIQUE constraint failed: core_answer.question_id")

    def test_question_state_from_incomplete(self):
        """Check that question state.

        Confirm that state can only go from 'incomplete' to
        'ready for review'.
        """
        question1 = Question.objects.all()[0]

        with pytest.raises(StateException) as exception_info:
            question1.change_to_needs_reworking()
        assert(exception_info.value.__str__() ==
               "Incorrect state change. Current state is 0")
        assert(question1.state == question1.INCOMPLETE)

        with pytest.raises(StateException) as exception_info:
            question1.change_to_complete()
        assert(exception_info.value.__str__() ==
               "Incorrect state change. Current state is 0")
        assert(question1.state == question1.INCOMPLETE)

        with pytest.raises(StateException) as exception_info:
            question1.change_to_flagged()
        assert(exception_info.value.__str__() ==
               "Incorrect state change. Current state is 0")
        assert(question1.state == question1.INCOMPLETE)

        question1.change_to_review_ready()
        assert(question1.state == question1.REVIEW_READY)

    def test_question_state_from_ready_for_review(self):
        """Check that question state.

        Confirm that state can only go from 'ready to review' to
        'complete' or 'needs reworking'.
        """
        question1 = Question.objects.all()[0]
        question1.state = question1.REVIEW_READY

        with pytest.raises(StateException) as exception_info:
            question1.change_to_review_ready()
        assert(exception_info.value.__str__() ==
               "Incorrect state change. Current state is 1")

        with pytest.raises(StateException) as exception_info:
            question1.change_to_flagged()
        assert(exception_info.value.__str__() ==
               "Incorrect state change. Current state is 1")
        assert(question1.state == question1.REVIEW_READY)

        question1.change_to_complete()
        assert(question1.state == question1.COMPLETE)

        question1.state = question1.REVIEW_READY

        question1.change_to_needs_reworking()
        assert(question1.state == question1.NEEDS_REWORKING)

    def test_question_state_from_needs_reworking(self):
        """Check that question state.

        Confirm that state can only go from 'needs reworking' to
        'ready for review'.
        """
        question1 = Question.objects.all()[0]
        question1.state = question1.NEEDS_REWORKING

        with pytest.raises(StateException) as exception_info:
            question1.change_to_needs_reworking()
        assert(exception_info.value.__str__() ==
               "Incorrect state change. Current state is 2")
        assert(question1.state == question1.NEEDS_REWORKING)

        with pytest.raises(StateException) as exception_info:
            question1.change_to_complete()
        assert(exception_info.value.__str__() ==
               "Incorrect state change. Current state is 2")
        assert(question1.state == question1.NEEDS_REWORKING)

        with pytest.raises(StateException) as exception_info:
            question1.change_to_flagged()
        assert(exception_info.value.__str__() ==
               "Incorrect state change. Current state is 2")
        assert(question1.state == question1.NEEDS_REWORKING)

        question1.change_to_review_ready()
        assert(question1.state == question1.REVIEW_READY)

    def test_question_state_from_complete(self):
        """Check that question state.

        Confirm that state can only go from 'complete' to
        'flagged for review'.
        """
        question1 = Question.objects.all()[0]
        question1.state = question1.COMPLETE

        with pytest.raises(StateException) as exception_info:
            question1.change_to_review_ready()
        assert(exception_info.value.__str__() ==
               "Incorrect state change. Current state is 3")
        assert(question1.state == question1.COMPLETE)

        with pytest.raises(StateException) as exception_info:
            question1.change_to_complete()
        assert(exception_info.value.__str__() ==
               "Incorrect state change. Current state is 3")
        assert(question1.state == question1.COMPLETE)

        with pytest.raises(StateException) as exception_info:
            question1.change_to_needs_reworking()
        assert(exception_info.value.__str__() ==
               "Incorrect state change. Current state is 3")
        assert(question1.state == question1.COMPLETE)

        question1.change_to_flagged()
        assert(question1.state == question1.FLAGGED)

    def test_question_state_from_flagged_for_review(self):
        """Check that question state.

        Confirm that state can only go from 'flagged for review' to
        'complete'.
        """
        question1 = Question.objects.all()[0]
        question1.state = question1.FLAGGED

        with pytest.raises(StateException) as exception_info:
            question1.change_to_review_ready()
        assert(exception_info.value.__str__() ==
               "Incorrect state change. Current state is 4")
        assert(question1.state == question1.FLAGGED)

        with pytest.raises(StateException) as exception_info:
            question1.change_to_needs_reworking()
        assert(exception_info.value.__str__() ==
               "Incorrect state change. Current state is 4")
        assert(question1.state == question1.FLAGGED)

        with pytest.raises(StateException) as exception_info:
            question1.change_to_flagged()
        assert(exception_info.value.__str__() ==
               "Incorrect state change. Current state is 4")
        assert(question1.state == question1.FLAGGED)

        question1.change_to_complete()
        assert(question1.state == question1.COMPLETE)
