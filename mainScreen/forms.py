from django import forms

class FraudDetectionForm(forms.Form):
    choose = forms.CharField(label='Input', max_length=100)
    Amount = forms.CharField(label='Input 2', max_length=100)
    Card = forms.CharField(label='Input 4', max_length=100)
    Errors = forms.CharField(label='Input 6', max_length=100)
    Merchant_city = forms.CharField(label='Input 4', max_length=100)
    Merchant_name = forms.CharField(label='Input 5', max_length=100)
    Merchant_state = forms.CharField(label='Input 6', max_length=100)
    Use_chip = forms.CharField(label='Input 7', max_length=100)
    User_profile = forms.CharField(label='Input 8', max_length=100)
    Zip = forms.CharField(label='Input 9', max_length=100)