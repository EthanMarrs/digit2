"""Models.py: creates models for core of digit platform."""
from django.db import models


class StateException(Exception):
    """An Exception when incorrect action is called on a given state."""

    def __init__(self, state):
        """Constructor for StateException."""
        self.state = state

    def __str__(self):
        """Return state error message indicating why exception is thrown."""
        return ("Incorrect state change. Current state is " +
                str(self.state))


class Grade(models.Model):
    """Grade class that describes school year."""

    name = models.TextField(max_length=10)


class Syllabus(models.Model):
    """Overarching container that conceptually organises topics for a year."""

    grade = models.OneToOneField(Grade)


class Topic(models.Model):
    """Class that describes a unit of math content with time and duration."""

    name = models.TextField(max_length=50)
    description = models.TextField(max_length=200)
    syllabus = models.ForeignKey(Syllabus)
    week_start = models.PositiveSmallIntegerField(unique=True)
    duration = models.PositiveSmallIntegerField()


class Block(models.Model):
    """Class that is used to organise math questions within a topic."""

    topic = models.ForeignKey(Topic)
    order = models.PositiveIntegerField(default=0)


class Subject(models.Model):
    """Class that describes the area of mathematics that a block covers."""

    name = models.TextField(max_length=50)
    grade = models.ForeignKey(Grade)


class Question(models.Model):
    """Question class containing challenge."""

    INCOMPLETE = 0
    REVIEW_READY = 1
    NEEDS_REWORKING = 2
    COMPLETE = 3
    FLAGGED = 4

    QUESTION_STATES = (
        (INCOMPLETE, "Incomplete"),
        (REVIEW_READY, "Ready for Review"),
        (NEEDS_REWORKING, "Needs Reworking"),
        (COMPLETE, "Complete"),
        (FLAGGED, "Flagged for review")
    )

    content = models.TextField()
    explanation = models.TextField()
    block = models.ForeignKey(Block)
    subject = models.ForeignKey(Subject)
    # WARNING: DO NOT CHANGE STATE DIRECTLY, USE STATE CHANGE METHODS
    state = models.PositiveIntegerField("State",
                                        choices=QUESTION_STATES,
                                        default=INCOMPLETE)

    def change_to_review_ready(self):
        """Change state of question.

        Changes state to "Ready for Review", only if in the state of
        "Incomplete"
        or "Needs Reworking".
        """
        if (self.state is self.INCOMPLETE or
                self.state is self.NEEDS_REWORKING):
            self.state = self.REVIEW_READY
        else:
            raise StateException(self.state)

    def change_to_needs_reworking(self):
        """Change state of question.

        Changes state to "Needs Reworking", only if in the state of
        "Ready for Review".
        """
        if self.state is self.REVIEW_READY:
            self.state = self.NEEDS_REWORKING
        else:
            raise StateException(self.state)

    def change_to_complete(self):
        """Change state of question.

        Changes state to "Complete", only if in the state of "Ready for Review"
        or "Flagged for Review".
        """
        if (self.state is self.REVIEW_READY or
                self.state is self.FLAGGED):
            self.state = self.COMPLETE
        else:
            raise StateException(self.state)

    def change_to_flagged(self):
        """Change state of question.

        Changes state to "Flagged", only if in the state of "Complete".
        """
        if self.state is self.COMPLETE:
            self.state = self.FLAGGED
        else:
            raise StateException(self.state)


class Answer(models.Model):
    """Single correct answer for each Question."""

    content = models.TextField()
    question = models.OneToOneField(Question)


class Option(models.Model):
    """One or more incorrect options for each Question."""

    content = models.TextField()
    question = models.ForeignKey(Question)
