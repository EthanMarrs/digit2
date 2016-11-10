from django.shortcuts import render
from django.views.generic import View, FormView
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.db.models import F
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError

from datetime import datetime, timedelta

from core import models
from student import forms


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

    def post(self, request, *args, **kwargs):
        question = request.POST["question"]  # Question ID
        answer = request.POST["answer"]  # Answer ID
        if question and answer:
            models.QuestionResponse.objects.create(
                question_id=question,
                answer_id=answer,
                user=request.user
            )
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)


class SignupView(FormView):
    template_name = "signup.html"
    success_url = "/quiz/"
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
