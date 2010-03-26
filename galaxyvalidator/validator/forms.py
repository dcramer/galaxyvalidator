from django import forms

class ValidateTextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(rows=50, cols=50))

class ValidateFileForm(forms.Form):
    file = forms.FileField()