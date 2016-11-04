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


class TopicForm(forms.Form):
    name = forms.CharField(widget=forms.Textarea())
    description = forms.CharField(widget=forms.Textarea())
    syllabus = forms.ModelChoiceField(queryset=models.Syllabus.objects.all())
    week_start = forms.IntegerField()
    duration = forms.IntegerField()
