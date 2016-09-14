from django.conf.urls import url
from django.views.generic import TemplateView

from core import views


urlpatterns = [
    url(r'^syllabi/(?P<pk>[^/]+)', views.SyllabusDetailView.as_view()),
    url(r'^question_orders/(?P<pk>[^/]+)', views.QuestionOrderDetailView.as_view()),
    url(r'^questions/(?P<pk>)/up[^/]', views.QuestionPositionUpView, name='up'),
    url(r'^comments/', views.CommentView.as_view()),
    url(r'^comment_success/', TemplateView.as_view(template_name='comment_success.html'))
]