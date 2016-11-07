from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render, HttpResponseRedirect
from django.db.models import F

from datetime import datetime, timedelta

from core import models, forms


class HomeView(View):
    """
    A simple view that displays the Dig-it welcome screen.
    Also has links to login and signup.
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect("/quiz/")
        else:
            return render(request, "home.html",
                          {"user": request.user})


class QuizView(View):
    """
    The view for students answering questions. This is a fairly complex view, since it
    needs to calculate which questions to show to a student.
    Firstly, the questions answered within the last 2 weeks are selected.
    Then the available questions for the last 2 weeks are selected.
    The answered questions are removed from the available pool.
    A question is randomly selected from the pool.
    """
    def get(self, request):
        user = request.user
        week = int(datetime.now().strftime("%V"))

        if user.is_authenticated():
            klass = models.Class.objects.filter(users=user).first()

            if not klass:
                return HttpResponseRedirect('/not_configured')

            syllabus = klass.syllabus

            # Get IDs of questions answered within the last 2 weeks
            answered = models.QuestionResponse.objects.filter(
                time__gte=datetime.now() - timedelta(weeks=2),
                user=user
            ).values_list("question", flat=True)

            # Get topics in last 2 weeks for given syllabus
            topics = models.Topic.objects.annotate(
                week_end=F("week_start") + F("duration")) \
                .filter(week_end__gte=week - 2, syllabus=syllabus)

            # Get blocks for these topics
            blocks = models.Block.objects.filter(topic__in=topics)

            # Get IDs of questions in last 2 weeks
            pool = models.Question.objects.filter(block__in=blocks, live=True) \
                .values_list("id", flat=True)

            # Get question to serve from pool - answered
            question_set = set(pool) - set(answered)
            question = None

            if question_set:
                question = models.Question.objects.get(id=question_set.pop())

            return render(request, "quiz.html", {"question": question})
        else:
            return HttpResponseRedirect('/login/')
