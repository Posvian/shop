from django.shortcuts import render, redirect
from src.mainapp.forms import SellerForm
from .models import Product, Feedback, Seller


#
def products_view(request):

    products: Product = Product.objects.select_related(
        "category", "brand", "seller"
    ).all()
    feedback = Feedback.objects.select_related("user", "product").all()
    context = {
        "products": products,
        "feedback": feedback,
    }
    return render(
        request=request,
        template_name="mainapp_template/products.html",
        context=context,
    )


def shops_view(request):
    shops: Seller = Seller.objects.all()
    context = {"shops": shops}

    return render(
        request=request,
        template_name="mainapp_template/shops.html",
        context=context,
    )


def add_seller_view(request):
    context = {}
    if request.method == "POST":
        form = SellerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            iin = form.cleaned_data["iin"]
            country = form.cleaned_data["country"]
            Seller.objects.create(name=name, iin=iin, country=country)
            return redirect("/mainapp/shops/")
        context["form"] = SellerForm(request.POST)

    else:
        context["form"] = SellerForm()

    return render(
        request=request,
        template_name="mainapp_template/seller_form.html",
        context=context,
    )
