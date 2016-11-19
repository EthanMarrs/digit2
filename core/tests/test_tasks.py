"""test_views.py: runs tests on the views for digit."""
import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from django.core import mail
from django.conf import settings

from core.tasks import due_tasks_reminder
from core.models import (Grade,
                         Subject,
                         Question,
                         Comment,
                         Option,
                         Topic,
                         Block,
                         Syllabus,
                         Task,
                         StateException,
                         CorrectOptionExistsError,
                         )


class CoreTasksTest(TestCase):
    """
    Test all core tasks.
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
        Task.objects.create(assigned_to=creator,
                            assigned_by=user,
                            moderator=moderator,
                            topic=topic,
                            due_date=date.today()+timedelta(days=5))

    def test_due_tasks_reminder(self):
        """
        Test that an email reminder gets sent out if there are tasks due
        within the next 7 days.
        """
        settings.CELERY_ALWAYS_EAGER = True
        due_tasks_reminder.apply()
        self.assertEqual(len(mail.outbox), 1)
