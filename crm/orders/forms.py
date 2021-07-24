from django import forms


class ReplyToCustomer(forms.Form):
    order_type = forms.CharField(max_length=255)
    order_type.widget = forms.TextInput(attrs={'placeholder':'Change order type'})

    order_status = forms.CharField(max_length=255)
    order_status.widget = forms.TextInput(attrs={'placeholder':'Change order status'})


class OrderWhatHappened(forms.Form):
    what_happened = forms.CharField()
    what_happened.widget = forms.TextInput(attrs={'type': 'text', 'id': 'what_happened',
                                                  'class': 'form-control', 'placeholder': 'what_happened', 'required': True, 'autofocus': True})
