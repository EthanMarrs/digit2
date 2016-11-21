from django import forms

from core import models


class CommentForm(forms.Form):
    """
    A simple form for creating a text comment.
    """
    text = forms.CharField(widget=forms.Textarea(attrs=
                                                 {"rows": 2,
                                                  "style": "resize:none;"
                                                  }),
                           label="")
    question_id = forms.CharField(widget=forms.HiddenInput())


class BlockDescriptionForm(forms.Form):
    """
    A simple form for updating a Block's description text.
    """
    text = forms.CharField(widget=forms.Textarea(attrs=
                                                 {"rows": 4,
                                                  "style": "resize:none;width:98%;"
                                                  }),
                           label="")
    block_id = forms.CharField(widget=forms.HiddenInput())


class TopicForm(forms.Form):
    """
    A complex form used in the topic creation wizard.
    Most fields are fairly standard, however the 'syllabus' field uses a ModelChoiceField.
    This displays all the current syllabi available.
    """
    name = forms.CharField(widget=forms.Textarea())
    description = forms.CharField(widget=forms.Textarea())
    syllabus = forms.ModelChoiceField(queryset=models.Syllabus.objects.all())
    week_start = forms.IntegerField(min_value=1, max_value=53)
    duration = forms.IntegerField(min_value=1, max_value=53)


class SyllabusForm(forms.Form):
    """
    A complex form used in the syllabus creation wizard.
    Most fields are fairly standard.
    """
    grade_name = forms.CharField(widget=forms.Textarea(attrs=
                                                       {"rows": 1,
                                                        "style": "resize:none;"
                                                        }))
    class_name = forms.CharField(widget=forms.Textarea(attrs=
                                                       {"rows": 1,
                                                        "style": "resize:none;"
                                                        }))


class QuestionEditForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(QuestionEditForm, self).__init__(*args, **kwargs)

    subject = forms.ModelChoiceField(queryset=models.Subject.objects.all(), label="")
