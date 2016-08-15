from django.db import models


class Question(models.Model):
    # Question States
    INCOMPLETE = 1
    REVIEW_READY = 2
    NEEDS_REWORKING = 3
    COMPLETE = 4
    FLAGGED = 5

    content = models.TextField()
    explanation = models.TextField()
    state = models.PositiveIntegerField("State",
                                        choices=(
                                            (INCOMPLETE, "Incomplete"),
                                            (REVIEW_READY, "Ready for Review"),
                                            (NEEDS_REWORKING, "Needs Reworking"),
                                            (COMPLETE, "Complete"),
                                            (FLAGGED, "Flagged for Review")
                                        ),
                                        default=INCOMPLETE)

    def change_to_review_ready(self):
        if self.state is not self.INCOMPLETE or self.state is not self.NEEDS_REWORKING:
            raise ("Incorrect state change. Current state is" + str(self.state))
        else:
            self.state = self.REVIEW_READY

    def change_to_needs_reworking(self):
        if self.state is not self.REVIEW_READY:
            raise ("Incorrect state change. Current state is" + str(self.state))
        else:
            self.state = self.NEEDS_REWORKING

    def change_to_complete(self):
        if self.state is not self.REVIEW_READY or self.state is not self.FLAGGED:
            raise ("Incorrect state change. Current state is" + str(self.state))
        else:
            self.state = self.COMPLETE

    def change_to_flagged(self):
        if self.state is not self.COMPLETE:
            raise ("Incorrect state change. Current state is" + str(self.state))
        else:
            self.state = self.FLAGGED


class Answer(models.Model):
    content = models.TextField()
    question = models.OneToOneField(Question)


class Option(models.Model):
    content = models.TextField()
    question = models.ForeignKey(Question)


