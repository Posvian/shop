from django.shortcuts import render
from .models import Product, Feedback


#
def task_1(request):

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
        template_name="mainapp_template/task_1.html",
        context=context,
    )
