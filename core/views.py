import json
import os
from datetime import datetime, timedelta, date

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View, DetailView, ListView, FormView
from django.forms import ValidationError
from django.contrib.auth.models import User
from django.db.models import Q, Count, Sum, Case, When, IntegerField
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core import models, forms
from mathcontentconverter import ContentHandler

from django.conf import settings


class TaskDetailView(DetailView):
    """
    Screen that displays all information for a specific task.
    Allows for moving of blocks, moderation etc.
    """

    model = models.Task
    template_name = "task.html"

    def get_context_data(self, **kwargs):
        """ Get context for all questions relating to a question order."""

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


class QuestionMoveBlockView(View):
    """
    A view that moves a question to the specified block.
    Returns 400 if the destination block doesn't exist.
    """
    def post(self, request, *args, **kwargs):
        block_order = request.POST["block"]
        question = models.Question.objects.get(pk=kwargs["pk"])
        blocks = models.Block.objects.filter(topic=question.block.topic)

        try:
            question.block = blocks[int(block_order)]
            question.save()
            return HttpResponse(status=200)
        except IndexError:
            return HttpResponse(status=400)


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

    def get_queryset(self, *args, **kwargs):
        results = []

        for syllabus in models.Syllabus.objects.all():
            classes = models.Class.objects.filter(syllabus=syllabus)
            topics = models.Topic.objects.filter(syllabus=syllabus)
            students = 0
            questions = 0

            for topic in topics:
                questions += topic.get_number_of_questions()

            for klass in classes:
                students += klass.users.count()

            results.append({"syllabus": syllabus,
                            "students": students,
                            "topics": topics.count(),
                            "questions": questions})
        return results


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


class QuestionContentView(View):
    """
    A View that accepts json to create and update question content.
    """

    def post(self, request, *args, **kwargs):
        """Post view for question content."""
        data = json.loads(request.body.decode(encoding='UTF-8'))
        ch = ContentHandler(
            src_image_file_path=os.path.join(settings.MEDIA_ROOT, "uploaded_media"),
            dest_image_file_path=os.path.join(settings.MEDIA_ROOT, "optimised_media"),
            reference_url=(settings.MEDIA_URL + "optimised_media"),
            katex_conversion_url=settings.KATEX_CONVERSION_URL,
            create_images=True,
            reuse_images=True
        )

        # get question object
        question = models.Question.objects.get(id=int(data["name"]))

        question.question_content = ch.get_formatted_content(data["question_content"])
        question.answer_content = ch.get_formatted_content(data["answer_explanation_content"])
        if "answer_explanation_content" in data:
            question.additional_info_content = ch.get_formatted_content(
                data["answer_explanation_content"])
        question.save()

        # delete old options
        # THIS MUST CHANGE FOR RELIABLE SAVING AND PROCESSING OF QUESTIONS
        for option in models.Option.objects.filter(question=question):
            option.delete()

        # create the options
        for i in range(1, 4):
            # format the content
            option_name = "option_content_" + str(i)
            formatted_content = ch.get_formatted_content(data[option_name])
            option = models.Option(
                question=question,
                # TODO refactor how to selec the correct answer
                correct=(data["correct"]==option_name),
                content=formatted_content)
            option.save()

        return JsonResponse(data={}, status=200)


class FileUploadView(View):
    """
    A View that processes image content.
    """

    def post(self, request, *args, **kwargs):
        """Post view for file uploads."""
        for file_name in request.FILES:

            file_object = request.FILES[file_name]
            file = os.path.join(settings.MEDIA_ROOT, "uploaded_media", file_name)
            with open(file, 'wb+') as destination:
                for chunk in file_object.chunks():
                    destination.write(chunk)

        return HttpResponse(status=200)


class GetQuestionContent(View):
    """
    A view to fetch image content.
    """

    def post(self, request, *args, **kwargs):
        pass


class MyTasksView(View):
    """
    A view that displays the tasks set for the user currently logged in.
    Only returns tasks that are still open.
    """
    def get(self, request, *args, **kwargs):
        tasks = models.Task.objects.filter(Q(assigned_to=request.user) |
                                           Q(moderator=request.user),
                                           open=True)

        return render(request, "my_tasks.html",
                      {"title": "My Tasks",
                       "user": request.user,
                       "has_permission": request.user.is_staff,
                       "site_url": "/",
                       "site_header": "Dig-it",
                       "task_list": tasks})
