from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search', 'class': 's-input'}), max_length=200, label='')