from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView
from mainapp.forms import SellerForm, FeedbackForm, ProductForm
from .models import Product, Feedback, Seller, Category, Brand
from .tasks import make_image


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
    from .tasks import add

    a = add.delay(5, 5)

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


def add_product_view(request):
    context = {}
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            name = request.POST["name"]
            description = request.POST["description"]
            stock_balance = request.POST["stock_balance"]
            price = request.POST["price"]
            category = request.POST["category"]
            brand = request.POST["brand"]
            seller = request.POST["seller"]
            weight = request.POST["weight"]
            if "image" in request.FILES:
                image = request.FILES["image"]
                product = Product(
                    name=name,
                    description=description,
                    stock_balance=stock_balance,
                    price=price,
                    category=Category.objects.get(id=int(category)),
                    brand=Brand.objects.get(id=int(brand)),
                    seller=Seller.objects.get(id=int(seller)),
                    weight=weight,
                    image=image,
                )
                product.save()
            else:
                make_image.delay(
                    name=name,
                    description=description,
                    stock_balance=stock_balance,
                    price=price,
                    category=category,
                    brand=brand,
                    seller=seller,
                    weight=weight,
                )
                return redirect("/mainapp/products/")
            context["form"] = ProductForm(request.POST)
    else:
        context["form"] = ProductForm()
    return render(request, "mainapp_template/create_product_form.html", context=context)


class FeedbackView(CreateView):
    template_name = "mainapp_template/feedback_form.html"
    form_class = FeedbackForm
    success_url = "/mainapp/products"
