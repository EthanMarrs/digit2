import json
from datetime import datetime, timedelta, date

from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View, DetailView, ListView, FormView
from django.forms import ValidationError
from django.contrib.auth.models import User
from django.db.models import Q, Count, Sum, Case, When, IntegerField

from core import models, forms


class TaskDetailView(DetailView):
    """ Overview screen for the Dig-it dashboard. Displays all syllabi."""

    model = models.Task
    template_name = "task.html"

    def get_context_data(self, **kwargs):
        """ Get context for all questions relating to a question order. """

        context = super(TaskDetailView, self).get_context_data(**kwargs)
        blocks = models.Block.objects.filter(topic=context["object"].topic)
        filter_option = self.request.GET.get('filter')

        if filter_option:
            filter_option = int(filter_option)

        context["block_list"] = blocks
        context['title'] = context['object']
        context['user'] = self.request.user
        context['has_permission'] = self.request.user.is_staff
        context['site_url'] = "/",
        context['site_header'] = "Dig-it"
        context['form'] = forms.BlockDescriptionForm
        context['filter'] = filter_option

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
        context['title'] = context['object']
        context['user'] = self.request.user
        context['has_permission'] = self.request.user.is_staff
        context['site_url'] = "/",
        context['site_header'] = "Dig-it"

        return context


class CommentView(View):
    def post(self, request, *args, **kwargs):
        text = request.POST["text"]
        question_id = kwargs["pk"]
        user = request.user

        models.Comment.objects.create(text=text,
                                      question_id=question_id,
                                      user=user)

        return HttpResponse(status=200)


class BlockView(View):
    def post(self, request, *args, **kwargs):
        text = request.POST["text"]
        block_id = kwargs["pk"]

        block = models.Block.objects.get(id=block_id)
        block.description = text
        block.save()

        return HttpResponse(status=200)

    def get(self, request, *args, **kwargs):
        block = models.Block.objects.get(id=kwargs["pk"])

        return render(request, "block.html",
                      {"object": block,
                       "title": block,
                       "user": request.user,
                       "has_permission": request.user.is_staff,
                       "site_url": "/",
                       "site_header": "Dig-it"})


class TopicDetailView(DetailView):
    """
    A detail view that displays the detail of a topic, namely
    the blocks associated with it.
    """

    model = models.Topic
    template_name = "topic.html"

    def get_context_data(self, **kwargs):
        """ Get context for a topic. """

        context = super(TopicDetailView, self).get_context_data(**kwargs)
        return context


class QuestionUpView(View):
    """
    A view that intelligently increments the ordering of a question.
    If the question is currently at the top of its block, then
    the question is moved to the bottom of the next block (if it exists).
    """

    def post(self, request, *args, **kwargs):
        question = models.Question.objects.get(pk=kwargs["pk"])
        first_question = models.Question.objects.filter(block=question.block).first()

        # At top of block, so move up to next block
        if question == first_question:
            block = models.Block.objects.get(pk=question.block.id)
            first_block = models.Block.objects.filter(topic=question.block.topic).first()

            # Not the top block, otherwise do nothing
            if block != first_block:
                new_block = models.Block.objects.get(topic=block.topic,
                                                     order=block.order - 1)
                pos = models.Question.objects.filter(block=new_block).count()

                question.block = new_block
                question.order = pos
                question.save()

        else:
            question.up()

        return HttpResponse(status=200)


class QuestionDownView(View):
    """
    A view that intelligently decrements the ordering of a question.
    If the question is currently at the bottom of its block, then
    the question is moved to the top of the next block (if it exists).
    """

    def post(self, request, *args, **kwargs):
        question = models.Question.objects.get(pk=kwargs["pk"])
        last_question = models.Question.objects.filter(block=question.block).last()

        # At bottom of block, so move down to previous block
        if question == last_question:
            block = models.Block.objects.get(pk=question.block.id)
            last_block = models.Block.objects.filter(topic=question.block.topic).last()

            # Not the bottom block, otherwise do nothing
            if block != last_block:
                new_block = models.Block.objects.get(topic=block.topic,
                                                     order=block.order + 1)
                pos = models.Question.objects.filter(block=new_block).count()

                question.block = new_block
                question.order = pos
                question.save()
                question.top()

        else:
            question.down()

        return HttpResponse(status=200)


class QuestionChangeStateView(View):
    """
    A view that updates a particular question's state.
    """

    def post(self, request, *args, **kwargs):
        question = models.Question.objects.get(pk=kwargs["pk"])
        value = request.POST["value"]

        changed = question.change_state(value)

        if changed:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)


class SyllabusTimelineView(View):
    def get(self, request, *args, **kwargs):
        syllabus = models.Syllabus.objects.get(pk=kwargs["pk"])
        topics = models.Topic.objects.filter(syllabus=syllabus).order_by("week_start")
        now = datetime.now()
        results = []

        for index, topic in enumerate(topics):
            spaced = False

            if index > 0:
                week_end = topics[index - 1].week_start + topics[index - 1].duration

                # If there's a space between two topics
                if (topic.week_start - 1) > week_end:
                    spaced = True

            results.append({
                "id": topic.id,
                "name": topic.name,
                "description": topic.description,
                "week_start": topic.week_start,
                "spaced": spaced,
                # "date_start": "",
                "space": topic.get_number_of_blocks() * 95,
                "number_of_blocks": topic.get_number_of_blocks(),
                "number_of_questions": topic.get_number_of_questions(),
                "duration": topic.duration,
                "week_end": topic.week_start + topic.duration - 1,
            })

        json_results = json.dumps(results)

        return render(request, "timeline.html",
                      {"syllabus": syllabus,
                       "title": syllabus,
                       "user": request.user,
                       "has_permission": request.user.is_staff,
                       "site_url": "/",
                       "site_header": "Dig-it",
                       "data": results,
                       "json": json_results})


class SyllabusListView(ListView):
    model = models.Syllabus
    template_name = "syllabi.html"

    def get_context_data(self, **kwargs):
        context = super(SyllabusListView, self).get_context_data(**kwargs)
        context['title'] = "Syllabus List"
        context['user'] = self.request.user
        context['has_permission'] = self.request.user.is_staff
        context['site_url'] = "/",
        context['site_header'] = "Dig-it"
        return context


class TaskListView(ListView):
    model = models.Task
    template_name = "tasks.html"

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context['title'] = "Task List"
        context['user'] = self.request.user
        context['has_permission'] = self.request.user.is_staff
        context['site_url'] = "/",
        context['site_header'] = "Dig-it"
        context['open'] = self.request.GET.get('open')
        context['assigned_to'] = self.request.GET.get('assigned_to')
        return context

    def get_queryset(self, *args, **kwargs):
        active_filter = self.request.GET.get('open')
        assigned_to = self.request.GET.get('assigned_to')

        # Filter based on assignment and open status
        if assigned_to:
            user = self.request.user

            if active_filter == 'true':
                return models.Task.objects.filter(open=True, assigned_to=user).order_by('-id')
            elif active_filter == 'false':
                return models.Task.objects.filter(open=False, assigned_to=user).order_by('-id')
            else:
                return models.Task.objects.filter(assigned_to=user).order_by('-id')

        else:
            if active_filter == 'true':
                return models.Task.objects.filter(open=True).order_by('-id')
            elif active_filter == 'false':
                return models.Task.objects.filter(open=False).order_by('-id')
            else:
                return models.Task.objects.all().order_by('-id')


class TaskLiveView(View):
    def post(self, *args, **kwargs):
        task = models.Task.objects.get(pk=kwargs["pk"])
        topic = task.topic

        for question in topic.get_questions():
            question.live = True
            question.save()

        return HttpResponse(status=200)


class TaskOpenView(View):
    def post(self, request, *args, **kwargs):
        task = models.Task.objects.get(pk=kwargs["pk"])
        state = request.POST["state"]

        if state == "true":
            task.open = True
        else:
            task.open = False

        task.save()

        return HttpResponse(status=200)


class QuestionEditView(View):
    def get(self, request, *args, **kwargs):
        question = models.Question.objects.get(id=kwargs["pk"])

        return render(request, "edit_question.html",
                      {"title": "Edit Question",
                       "user": request.user,
                       "has_permission": request.user.is_staff,
                       "site_url": "/",
                       "site_header": "Dig-it",
                       "form": forms.CommentForm,
                       "question": question})


class TopicCreateWizardView(FormView):
    template_name = "topic_create_wizard.html"
    success_url = "/admin/"
    form_class = forms.TopicForm

    def get_context_data(self, **kwargs):
        context = super(TopicCreateWizardView, self).get_context_data(**kwargs)
        context['title'] = "Topic Creation Wizard"
        context['user'] = self.request.user
        context['has_permission'] = self.request.user.is_staff
        context['site_url'] = "/",
        context['site_header'] = "Dig-it"

        syllabus_id = self.request.GET.get("syllabus")

        if syllabus_id:
            syllabus = models.Syllabus.objects.get(id=syllabus_id)
            context['syllabus'] = syllabus_id
        else:
            syllabus = models.Syllabus.objects.first()

        topics = models.Topic.objects.filter(syllabus=syllabus).order_by("week_start")
        results = []

        for index, topic in enumerate(topics):

            results.append({
                "id": topic.id,
                "name": topic.name,
                "week_start": topic.week_start,
                "duration": topic.duration,
                "week_end": topic.week_start + topic.duration - 1,
            })

        json_results = json.dumps(results)
        context['weeks'] = json_results

        return context

    def form_valid(self, form):
        topic = models.Topic(
            name=form.cleaned_data['name'],
            description=form.cleaned_data['description'],
            syllabus=form.cleaned_data['syllabus'],
            week_start=form.cleaned_data['week_start'],
            duration=form.cleaned_data['duration']
        )

        try:
            topic.save()
        except ValidationError:
            pass

        return super(TopicCreateWizardView, self).form_valid(form)


class StudentScoresView(View):
    """
    A view that displays the student scores for the week.
    """
    def get(self, request, *args, **kwargs):
        # Get week starting date
        now = date.today()
        week_start = now - timedelta(now.weekday())

        # Fetch all users that responded this week
        student_list = models.QuestionResponse.objects.filter(time__gte=week_start)\
            .values('user', 'user__username', 'user__first_name', 'user__last_name')\
            .annotate(responses=Count('user'),
                      correct=Sum(
                          Case(When(correct=True, then=1)),
                          output_field=IntegerField()
                      ))

        return render(request, "student_scores.html",
                      {"title": "Student Scores",
                       "user": request.user,
                       "has_permission": request.user.is_staff,
                       "site_url": "/",
                       "site_header": "Dig-it",
                       "student_list": student_list})


class MyWorkView(View):
    """
    A view that displays the tasks set for the user currently logged in.
    Only returns tasks that are still open.
    """
    def get(self, request, *args, **kwargs):
        tasks = models.Task.objects.filter(Q(assigned_to=request.user) |
                                           Q(moderator=request.user),
                                           open=True)
        print(tasks)

        return render(request, "my_work.html",
                      {"title": "My Work",
                       "user": request.user,
                       "has_permission": request.user.is_staff,
                       "site_url": "/",
                       "site_header": "Dig-it",
                       "task_list": tasks})
