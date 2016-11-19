# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.models import Task
from digit.celery import app
from datetime import datetime, timedelta, date
from django.core.mail import send_mail


@app.task()
def due_tasks_reminder():
    today = datetime.today()
    tasks = Task.objects.filter(due_date__range=(today, today + timedelta(days=7)))

    for task in tasks:
        if task.assigned_to.email:
            send_mail(
                'Reminder: Task Almost Due',
                'This is a reminder than the task "{}" is due within the next week.'.format(task),
                'notifications@dig-it.me',
                [task.assigned_to.email],
                fail_silently=False,
            )
