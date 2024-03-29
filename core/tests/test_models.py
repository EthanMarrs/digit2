"""test_models.py: runs tests on the models for digit."""
import pytest
from core.models import (Grade,
                         Subject,
                         Question,
                         Comment,
                         Option,
                         Topic,
                         Block,
                         Syllabus,
                         StateException,
                         )
from django.test import TestCase
from django.contrib.auth.models import User


class TestQuestion(TestCase):
    """Test the Question Model."""

    def setUp(self):
        """Create questions for testing."""
        grade_test = Grade(name="Grade Example")
        grade_test.save()
        subject_test = Subject(name="addition",
                               grade=grade_test)
        subject_test.save()
        question1 = Question(question_content='what is 1 + 1?',
                             answer_content='This is an addition question',
                             subject=subject_test)
        question1.save()

    def test_question_default_state(self):
        """Confirm that default state is Incomplete."""
        question1 = Question.objects.all()[0]
        assert(question1.state == question1.INCOMPLETE)

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

    def test_question_option_save(self):
        """Test that question cannot have option with correct answer."""
        question1 = Question.objects.all()[0]

        option = Option.objects.first()
        option.correct = True
        option.save()

        assert(len(question1.option_set.all()) == 3)
        assert(len(Option.objects.all()) == 3)

    def test_get_comments(self):
        """
        Test that the get_comments() function returns all comments
        relating to a question.
        """
        user = User.objects.create(username="testuser")
        question1 = Question.objects.all()[0]
        Comment.objects.create(text="Test comment!", question=question1, user=user)
        Comment.objects.create(text="Another comment!", question=question1, user=user)

        assert(len(question1.get_comments()) == 2)
        assert(question1.get_comments()[0].text == "Test comment!")
        assert(question1.get_comments()[0].created_at < question1.get_comments()[1].created_at)

    def test_get_options(self):
        """
        Test that the get_options() function returns all options
        relating to a question.
        """
        question1 = Question.objects.all()[0]

        assert(question1.get_number_of_options() == 3)

    def test_get_state(self):
        question1 = Question.objects.all()[0]

        assert(question1.state == question1.INCOMPLETE)
        assert(question1.get_state() == "Incomplete")


class TestTopic(TestCase):
    """Test the Topic Model."""

    def setUp(self):
        """Create Topic for testing."""

        grade_test = Grade.objects.create(name="Grade Example")
        syllabus_test = Syllabus.objects.create(grade=grade_test)
        Topic.objects.create(name="Financial Mathematics",
                             description="Topic that involves sinking funds "
                                         "and loan calculations",
                             syllabus=syllabus_test, week_start=1,
                             duration=3)

    def test_topic_creates_blocks(self):
        """
        Confirm that blocks are created automatically and associated with the
        topic.
        """
        blocks = Block.objects.all()
        assert(len(blocks) == 3)
        assert(blocks[0].topic.name == "Financial Mathematics")

    def test_topic_creates_questions(self):
        """
        Confirm that questions are created automatically and associated with the
        correct block and topic.
        """
        questions = Question.objects.all()
        assert(len(questions) == 3 * 15)
        assert(questions[0].block.topic.name == "Financial Mathematics")

    def test_topic_number_of_questions(self):
        """
        Confirm that the correct number of questions is returned by the helper
        function.
        """
        questions = Question.objects.all()
        topics = Topic.objects.all()
        assert(len(questions) == topics[0].get_number_of_questions())

    def test_topic_number_of_blocks(self):
        """
        Confirm that the correct number of blocks is returned by the helper
        function.
        """
        blocks = Block.objects.all()
        topics = Topic.objects.all()
        assert(len(blocks) == topics[0].get_number_of_blocks())

    def test_topic_save_does_not_duplicate_questions(self):
        already_created_topic = Topic.objects.get(name="Financial Mathematics")
        count = 0
        for block in Block.objects.filter(topic=already_created_topic):
            for question in Question.objects.filter(block=block):
                count += 1
        assert(count == 45)
        new_description = "This is a new description"
        already_created_topic.description = new_description
        already_created_topic.save()

        edited_topic = Topic.objects.get(name="Financial Mathematics")
        count = 0
        for block in Block.objects.filter(topic=edited_topic):
            for question in Question.objects.filter(block=block):
                count += 1
        assert(count == 45)
