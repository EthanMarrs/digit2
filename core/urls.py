from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.views import login, logout

from core import views


urlpatterns = [
    url(r'^$', views.QuizView.as_view()),
    url(r'^login/$', login, {'template_name': 'admin/login.html'}),
    url(r'^logout/$', logout),
    url(r'^question_orders/(?P<pk>[^/]+)', views.QuestionOrderDetailView.as_view()),
    url(r'^question_orders/', views.QuestionOrderListView.as_view()),
    url(r'^questions/(?P<pk>[^/]+)/up/', views.QuestionUpView.as_view()),
    url(r'^questions/(?P<pk>[^/]+)/down/', views.QuestionDownView.as_view()),
    url(r'^questions/(?P<pk>[^/]+)/state/', views.QuestionChangeStateView.as_view()),
    url(r'^questions/(?P<pk>[^/]+)/edit/', views.QuestionEditView.as_view()),
    url(r'^syllabi/(?P<pk>[^/]+)/timeline/', views.SyllabusTimelineView.as_view()),
    url(r'^syllabi/(?P<pk>[^/]+)', views.SyllabusDetailView.as_view()),
    url(r'^syllabi/', views.SyllabusListView.as_view()),
    url(r'^comments/(?P<pk>[^/]+)', views.CommentView.as_view()),
    url(r'^blocks/(?P<pk>[^/]+)', views.BlockView.as_view()),
    url(r'^comment_success/', TemplateView.as_view(template_name='comment_success.html')),
    url(r'^blocks/(?P<pk>[^/]+)', views.BlockDetailView.as_view()),
    url(r'^topics/(?P<pk>[^/]+)', views.TopicDetailView.as_view()),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^not_configured/', TemplateView.as_view(template_name='not_configured.html'))
]
