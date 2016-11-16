from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from core import views


urlpatterns = [
    url(r'^tasks/(?P<pk>[^/])/live/', login_required(views.TaskLiveView.as_view())),
    url(r'^tasks/(?P<pk>[^/])/open/', login_required(views.TaskOpenView.as_view())),
    url(r'^tasks/(?P<pk>[^/])', login_required(views.TaskDetailView.as_view())),
    url(r'^tasks/$', login_required(views.TaskListView.as_view())),
    url(r'^questions/(?P<pk>[^/]+)/up/', login_required(views.QuestionUpView.as_view())),
    url(r'^questions/(?P<pk>[^/]+)/down/', login_required(views.QuestionDownView.as_view())),
    url(r'^questions/(?P<pk>[^/]+)/state/', login_required(views.QuestionChangeStateView.as_view())),
    url(r'^questions/(?P<pk>[^/]+)/edit/', login_required(views.QuestionEditView.as_view())),
    url(r'^syllabi/(?P<pk>[^/]+)/timeline/', login_required(views.SyllabusTimelineView.as_view())),
    url(r'^syllabi/(?P<pk>[^/]+)', login_required(views.SyllabusDetailView.as_view())),
    url(r'^syllabi/', login_required(views.SyllabusListView.as_view())),
    url(r'^comments/(?P<pk>[^/]+)', login_required(views.CommentView.as_view())),
    url(r'^blocks/(?P<pk>[^/]+)', login_required(views.BlockView.as_view())),
    url(r'^comment_success/', login_required(TemplateView.as_view(template_name='comment_success.html'))),
    url(r'^topics/(?P<pk>[^/]+)', login_required(views.TopicDetailView.as_view())),
    url(r'^topic_create_wizard/', login_required(views.TopicCreateWizardView.as_view())),
    url(r'^student_scores/', login_required(views.StudentScoresView.as_view()))
]
