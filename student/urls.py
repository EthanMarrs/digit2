from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.views import login, logout

from student import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view()),
    url(r'^quiz/', views.QuizView.as_view()),
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', logout),
    url(r'^not_configured/', TemplateView.as_view(template_name='not_configured.html')),
    url(r'^welcome/', TemplateView.as_view(template_name='welcome.html')),
    url(r'^signup/', views.SignupView.as_view())
]
