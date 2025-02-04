from django.shortcuts import render
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
