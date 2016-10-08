from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required

from core import views


urlpatterns = [
    url(r'^$', views.QuizView.as_view()),
    url(r'^login/$', login, {'template_name': 'admin/login.html'}),
    url(r'^logout/$', logout),
    url(r'^syllabi/(?P<pk>[^/]+)', views.SyllabusDetailView.as_view()),
    url(r'^question_orders/(?P<pk>[^/]+)', views.QuestionOrderDetailView.as_view()),
    url(r'^questions/(?P<pk>[^/]+)/up/', views.QuestionUpView.as_view()),
    url(r'^questions/(?P<pk>[^/]+)/down/', views.QuestionDownView.as_view()),
    url(r'^questions/(?P<pk>[^/]+)/state/', views.QuestionChangeStateView.as_view()),
    url(r'^syllabi/', views.SyllabiView.as_view()),
    url(r'^comments/', views.CommentView.as_view()),
    url(r'^comment_success/', TemplateView.as_view(template_name='comment_success.html')),
    url(r'^blocks/(?P<pk>[^/]+)', views.BlockDetailView.as_view())
]
