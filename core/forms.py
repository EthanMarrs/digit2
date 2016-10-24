from django import forms


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