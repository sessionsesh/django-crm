from django import forms


class OrderWhatHappened(forms.Form):
    what_happened = forms.CharField()
    what_happened.widget = forms.TextInput(attrs={'type': 'text', 'id': 'what_happened',
                                                  'class': 'form-control', 'placeholder': 'what_happened', 'required': True, 'autofocus': True})
