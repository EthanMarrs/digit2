# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.models import Task, Topic
from digit.celery import app
from datetime import datetime, timedelta, date
from django.core.mail import send_mail
from django.db.models import F, Q
from django.conf import settings


@app.task()
def due_tasks_reminder():
    today = datetime.today()
    tasks = Task.objects.filter(due_date__range=(today, today + timedelta(days=7)))

    for task in tasks:
        if task.assigned_to.email:
            send_mail(
                'Dig-it Reminder: Task Almost Due',
                'This is a reminder than the task "{}" is due within the next week.'.format(task),
                'notifications@dig-it.me',
                [task.assigned_to.email],
                fail_silently=False,
            )


@app.task()
def content_missing_warning():
    problem_topics = []

    # Fetch the current week in ISO standard
    week = int(datetime.now().strftime("%V"))

    # Get topics scheduled for next week
    # Either the topic starts next week
    # Or the we are in the middle of the topic
    topic_list = Topic.objects.annotate(
        week_end=F("week_start") + F("duration")) \
        .filter(Q(week_start=week) | (Q(week_start__lt=week) & Q(week_end__gt=week)))

    if topic_list.count() < 1:
        return

    for topic in topic_list:
        if topic.get_number_of_live_questions() < 15 * topic.duration:
            problem_topics.append(topic)

    if len(problem_topics) > 0:
        topic_str = ""

        for topic in problem_topics:
            topic_str += topic.name + ", "

        send_mail(
            'Dig-it Warning: Content Might Be Missing',
            'This is a warning that the following topics may be missing content: {} '.format(topic_str),
            'notifications@dig-it.me',
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
