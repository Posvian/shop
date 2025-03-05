# from rest_framework import generics
#
# from authapp.models import CustomUser
# from shop_api.serializers import CustomUserSerializer
#
#
# class UserAPIView(generics.ListAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from authapp.models import CustomUser
from shop_api.serializers import CustomUserSerializer


@csrf_exempt
def custom_user_list(request):
    if request.method == "GET":
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def custom_user_detail(request, pk):
    try:
        user = CustomUser.objects.get(id=pk)
    except CustomUser.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = CustomUserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = CustomUserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        user.delete()
        return HttpResponse(status=204)
