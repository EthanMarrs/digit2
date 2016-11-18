from django.forms import ModelForm, PasswordInput
from django import forms
from django.contrib.auth.models import User


class SignupForm(ModelForm):
    """
    A simple signup form that allows students to register with Dig-it.
    """

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'password': PasswordInput(),
        }
        labels = {
            'first_name': 'Name',
            'last_name': 'Surname',
            'email': 'Email'
        }
        help_texts = {
            'username': None
        }


class QuizForm(forms.Form):
    """
    A form for submitting responses to a question.
    """

    # def __init__(self, *args, **kwargs):
    #     super(QuizForm, self).__init__(**kwargs)
    #     options = kwargs.pop("options")
    #     print(options)
    #     self.fields["option"] = forms.RadioSelect(choices=options)

    question = forms.IntegerField(widget=forms.HiddenInput())
    # option = forms.RadioSelect()
