from datetime import datetime

from django import template
from django.db.models import F, Q

from core import models

register = template.Library()


@register.simple_tag
def need_reminder():
    """
    A template tag which checks if there is enough content for the
    upcoming week. Returns True if a reminder is needed to fix
    content, or False if not.
    """
    flag = False

    # Fetch the current week in ISO standard
    week = int(datetime.now().strftime("%V"))

    # Get topics scheduled for next week
    # Either the topic starts next week
    # Or the we are in the middle of the topic
    topic_list = models.Topic.objects.annotate(
        week_end=F("week_start") + F("duration")) \
        .filter(Q(week_start=week) | (Q(week_start__lt=week) & Q(week_end__gt=week)))

    if topic_list.count() < 1:
        return True

    for topic in topic_list:
        if topic.get_number_of_live_questions() < 15 * topic.duration:
            flag = True

    return flag

