from django.shortcuts import render
from django.views.generic import View, DetailView
from django.utils import timezone

from core import models


class DashboardAdminView(View):
    """ Overview screen for the Digit dashboard. Displays all syllabi."""

    def get(self, request):
        syllabi_list = models.Syllabus.objects.all()
        return render(request, "dashboard.html", {"syllabi": syllabi_list})


class QuestionOrderDetailView(DetailView):
    """ Overview screen for the Digit dashboard. Displays all syllabi."""

    model = models.QuestionOrder
    template_name = "question_order.html"

    def get_context_data(self, **kwargs):
        """ Get context for all questions relating to a question order. """

        context = super(QuestionOrderDetailView, self).get_context_data(**kwargs)
        context["question_list"] = models.Question.objects.filter(
            question_order=context["object"]
        )

        return context


class SyllabiDetailView(DetailView):
    """ Displays all modules and associated questions of a Syllabus. """

    model = models.Syllabus
    template_name = "syllabus.html"
