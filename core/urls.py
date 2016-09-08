from django.conf.urls import url

from core import views


urlpatterns = [
    url(r'^syllabi/(?P<pk>[^/]+)', views.SyllabiDetailView.as_view()),
    url(r'^question_orders/(?P<pk>[^/]+)', views.QuestionOrderDetailView.as_view()),
]