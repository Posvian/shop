from cProfile import label

from django import forms
from mainapp.models import Feedback
from mainapp.models import Product


class SellerForm(forms.Form):
    name = forms.CharField(max_length=40, label="Your shop name")
    iin = forms.CharField(max_length=12, label="Your iin")
    country = forms.CharField(max_length=50, label="Your country")


class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].empty_label = "Пользователь не выбран"
        self.fields["product"].empty_label = "Продукт не выбран"

    class Meta:
        model = Feedback
        fields = ["user", "product", "feedback", "rating"]
        widgets = {"feedback": forms.Textarea(attrs={"cols": 60, "rows": 10})}


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "stock_balance",
            "price",
            "category",
            "brand",
            "seller",
            "weight",
            "image",
        ]
        widgets = {"description": forms.Textarea(attrs={"cols": 60, "rows": 10})}
