import json
from datetime import datetime, timedelta

from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View, DetailView, ListView, FormView
from django.forms import ValidationError

from core import models, forms


class QuestionOrderDetailView(DetailView):
    """ Overview screen for the Digit dashboard. Displays all syllabi."""

    model = models.QuestionOrder
    template_name = "question_order.html"

    def get_context_data(self, **kwargs):
        """ Get context for all questions relating to a question order. """

        context = super(QuestionOrderDetailView, self).get_context_data(**kwargs)
        blocks = models.Block.objects.filter(topic=context["object"].topic)
        filter_option = self.request.GET.get('filter')

        if filter_option:
            filter_option = int(filter_option)

        context["block_list"] = blocks
        context['title'] = context['object']
        context['user'] = self.request.user
        context['has_permission'] = self.request.user.is_staff
        context['site_url'] = "/",
        context['site_header'] = "Digit"
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
        context['site_header'] = "Digit"

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
                       "site_header": "Digit"})


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


class QuizView(View):
    def get(self, request):
        user = request.user
        week = int(datetime.now().strftime("%V"))

        if user.is_authenticated:
            klass = models.Class.objects.get(users=user)
            syllabus = klass.syllabus

            if not syllabus:
                return HttpResponseRedirect('/not_configured')

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
                       "site_header": "Digit",
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
        context['site_header'] = "Digit"
        return context


class QuestionOrderListView(ListView):
    model = models.QuestionOrder
    template_name = "question_orders.html"

    def get_context_data(self, **kwargs):
        context = super(QuestionOrderListView, self).get_context_data(**kwargs)
        context['title'] = "Question Order List"
        context['user'] = self.request.user
        context['has_permission'] = self.request.user.is_staff
        context['site_url'] = "/",
        context['site_header'] = "Digit"
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
                return models.QuestionOrder.objects.filter(open=True, assigned_to=user).order_by('-id')
            elif active_filter == 'false':
                return models.QuestionOrder.objects.filter(open=False, assigned_to=user).order_by('-id')
            else:
                return models.QuestionOrder.objects.filter(assigned_to=user).order_by('-id')

        else:
            if active_filter == 'true':
                return models.QuestionOrder.objects.filter(open=True).order_by('-id')
            elif active_filter == 'false':
                return models.QuestionOrder.objects.filter(open=False).order_by('-id')
            else:
                return models.QuestionOrder.objects.all().order_by('-id')


class QuestionOrderLiveView(View):
    def post(self, *args, **kwargs):
        question_order = models.QuestionOrder.objects.get(pk=kwargs["pk"])
        topic = question_order.topic

        for question in topic.get_questions():
            question.live = True
            question.save()

        return HttpResponse(status=200)


class QuestionOrderOpenView(View):
    def post(self, request, *args, **kwargs):
        question_order = models.QuestionOrder.objects.get(pk=kwargs["pk"])
        state = request.POST["state"]

        if state == "true":
            question_order.open = True
        else:
            question_order.open = False

        question_order.save()

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

