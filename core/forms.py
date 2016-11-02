from django import forms

from core import models


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs=
                                                 {"rows": 2,
                                                  "style": "resize:none;"
                                                  }),
                           label="")
    question_id = forms.CharField(widget=forms.HiddenInput())


class BlockDescriptionForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs=
                                                 {"rows": 4,
                                                  "style": "resize:none;width:98%;"
                                                  }),
                           label="")
    block_id = forms.CharField(widget=forms.HiddenInput())


def fetch_syllabi():
    choices = models.Syllabus.objects.all().values_list('grade__id', 'grade__name')
    result = []

    for grade in choices:
        result.append((grade[0], "Grade " + grade[1] + " Syllabus"))

    return result


class TopicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields['syllabus'] = forms.ChoiceField(
            choices=fetch_syllabi())

    name = forms.CharField(widget=forms.Textarea())
    description = forms.CharField(widget=forms.Textarea())
    syllabus = forms.ChoiceField(choices=fetch_syllabi())
    week_start = forms.IntegerField()
    duration = forms.IntegerField()
