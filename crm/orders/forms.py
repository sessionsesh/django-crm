from django import forms


class ReplyToCustomer(forms.Form):
    # order_id = forms.IntegerField()
    order_type = forms.CharField(max_length=255, required=False)
    order_type.widget = forms.TextInput(attrs={'placeholder':'Change order type'})

    order_status = forms.CharField(max_length=255, required=False)
    order_status.widget = forms.TextInput(attrs={'placeholder':'Change order status'})


class OrderWhatHappened(forms.Form):
    what_happened = forms.CharField()
    what_happened.widget = forms.TextInput(attrs={'type': 'text', 'id': 'what_happened',
                                                  'class': 'form-control', 'placeholder': 'what_happened', 'required': True, 'autofocus': True})

class NewCustomerNewOrder(forms.Form):
    what_happened = forms.CharField()
    what_happened.widget = forms.TextInput(attrs={})

    phone_number = forms.CharField()
    phone_number.widget = forms.TextInput(attrs={})