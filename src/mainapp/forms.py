from django import forms


class SellerForm(forms.Form):
    name = forms.CharField(max_length=40, label="Your shop name")
    iin = forms.CharField(max_length=12, label="Your iin")
    country = forms.CharField(max_length=50, label="Your country")
