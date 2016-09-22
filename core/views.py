from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View, DetailView
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import F

from core import models, forms


class DashboardView(View):
    """ Overview screen for the Digit dashboard. Displays all syllabi."""

    def get(self, request):
        syllabi_list = models.Syllabus.objects.all()
        return render(request, "dashboard.html", {"syllabi": syllabi_list})


class QuestionOrderDetailView(DetailView):
    """ Overview screen for the Digit dashboard. Displays all syllabi."""

    model = models.QuestionOrder
    template_name = "question_order.html"
    form_class = forms.CommentForm

    def get_context_data(self, **kwargs):
        """ Get context for all questions relating to a question order. """

        context = super(QuestionOrderDetailView, self).get_context_data(**kwargs)
        context["question_list"] = models.Question.objects.filter(
            question_order=context["object"]
        )
        context["form"] = self.form_class

        return context


class SyllabusDetailView(DetailView):
    """ Displays all modules and associated questions of a Syllabus. """

    model = models.Syllabus
    template_name = "syllabus.html"

    def get_context_data(self, **kwargs):
        """ Get context for a syllabus. """

        context = super(SyllabusDetailView, self).get_context_data(**kwargs)
        context["topic_list"] = models.Topic.objects.filter(
            syllabus=context["object"]
        )

        return context


class CommentView(View):
    form_class = forms.CommentForm
    initial = {"key": "value"}
    template_name = "question_form.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            question_id = form.cleaned_data["question_id"]
            user = request.user

            models.Comment.objects.create(text=text,
                                          question_id=question_id,
                                          user=user)

            return HttpResponseRedirect("/comment_success")

        return render(request, self.template_name, {'form': form})


class BlockDetailView(DetailView):
    """
    A detail view that displays the detail of a block, namely
    the questions associated with it.
    """

    model = models.Block
    template_name = "block.html"

    def get_context_data(self, **kwargs):
        """ Get context for a block. """

        context = super(BlockDetailView, self).get_context_data(**kwargs)
        return context


class QuizView(View):
    def get(self, request):
        user = request.user
        week = int(datetime.now().strftime("%V"))

        syllabus = models.Syllabus.objects.filter(users=user)[0]

        # Get IDs of questions answered within the last 2 weeks
        answered = models.QuestionResponse.objects.filter(
            time__gte=datetime.now()-timedelta(weeks=2),
            user=user
        ).values_list("question", flat=True)

        # Get topics in last 2 weeks for given syllabus
        topics = models.Topic.objects.annotate(
            week_end=F("week_start") + F("duration"))\
            .filter(week_end__gte=week - 2, syllabus=syllabus)

        # Get blocks for these topics
        blocks = models.Block.objects.filter(topic__in=topics)

        # Get IDs of questions in last 2 weeks
        pool = models.Question.objects.filter(block__in=blocks)\
            .values_list("id", flat=True)

        # Get question to serve from pool - answered
        question_set = set(pool) - set(answered)
        question = None

        if question_set:
            question = models.Question.objects.get(id=question_set.pop())

        return render(request, "quiz.html", {"question": question})


