from django.shortcuts import render
from django.views.generic import View, FormView
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.db.models import F
from django.contrib.auth.models import User
from django.forms import ValidationError

from datetime import date, datetime, timedelta
from random import randint

from core import models
from student import forms

import random


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

            # Get number of responses today
            responses_today = models.QuestionResponse.objects.filter(
                time__gte=date.today(),
                user=user
            ).count()

            # If max reached, don't give question
            if responses_today > 2:
                return render(request, "quiz.html", {"question": None})

            syllabus = klass.syllabus

            # Get IDs of questions answered within the last 2 weeks
            answered = models.QuestionResponse.objects.filter(
                time__gte=datetime.now() - timedelta(weeks=2),
                user=user
            ).values_list("question", flat=True)

            # Get topics in last 2 weeks for given syllabus
            topics = models.Topic.objects.annotate(
                week_end=F("week_start") + F("duration") - 1) \
                .filter(week_end__gte=week - 2, syllabus=syllabus)

            # Get blocks for these topics
            blocks = models.Block.objects.filter(topic__in=topics)

            # Get IDs of questions in last 2 weeks
            pool = models.Question.objects.filter(block__in=blocks, live=True) \
                .values_list("id", flat=True)

            # Get question to serve from pool - answered
            question_set = list(set(pool) - set(answered))
            question = None

            if question_set:
                question = models.Question.objects.get(id=question_set[randint(0, len(question_set) - 1)])
                # .order_by('?') enforces business rule
                # that options are randomly ordered
                options = models.Option.objects.filter(question=question).order_by('?')
                form = forms.QuizForm(initial={"question": question.id, "options": options})
            else:
                options = None
                form = forms.QuizForm()

            return render(request, "quiz.html",
                          {"question": question,
                           "options": options,
                           "form": form})
        else:
            return HttpResponseRedirect('/login/')

    def post(self, request, *args, **kwargs):
        # TODO handle conversion error
        question_id = int(request.POST["question"])  # Question ID
        option_id = int(request.POST["option"])  # Option ID
        option = models.Option.objects.get(id=option_id)

        if question_id and option:
            models.QuestionResponse.objects.create(
                question_id=question_id,
                response=option,
                correct=option.correct,
                user=request.user
            )
            # return
            options = models.Option.objects.filter(question_id=question_id)
            correct_option = None
            for _option in options:
                if _option.correct:
                    correct_option = _option
                    break

            question = models.Question.objects.get(id=question_id)
            return render(request, "quiz_response.html",
                          {"True": True,
                           "False": False,
                           "options": options,
                           "question": question,
                           "selected_option": option,
                           "correct_option": correct_option,
                           "response_correct": option.correct})
        else:
            return HttpResponse(status=400)


class SignupView(FormView):
    template_name = "signup.html"
    success_url = "/welcome/"
    form_class = forms.SignupForm

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )

        try:
            user.save()
        except ValidationError:
            pass

        return super(SignupView, self).form_valid(form)
