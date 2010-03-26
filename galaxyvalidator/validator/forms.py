from django import forms

class ValidateTextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs=dict(rows=15, cols=100)))

class ValidateFileForm(forms.Form):
    file = forms.FileField()