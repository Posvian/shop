from django.shortcuts import render
from .models import Product


# def product_list(request):
#     products = (
#         Product.objects.select_related("brand")
#         .select_related("category")
#         .all()
#     )
#
#     context = {"products": products}
#     return render(request=request, template_name="mainapp_template/base.html", context=context)
