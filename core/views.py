from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View, DetailView
from django.utils import timezone

from core import models, forms


class DashboardAdminView(View):
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
