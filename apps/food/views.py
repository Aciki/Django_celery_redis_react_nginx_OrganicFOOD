# Create your views here.
import logging

import django_filters
from django.db.models import query
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import FoodNotFound
from .models import Food, FoodViews
from .pagination import FoodPagination
from .serializers import (FoodCreateSerializer, FoodSerializer,
                          FoodViewSerializer)

logger = logging.getLogger(__name__)


class FoodFilter(django_filters.FilterSet):

   

    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        model = Food
        fields = ["price"]


class ListAllFoodAPIView(generics.ListAPIView):
    serializer_class = FoodSerializer
    queryset = Food.objects.all().order_by("-created_at")
    pagination_class = FoodPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = FoodFilter
    search_fields = ["country", "city"]
    ordering_fields = ["created_at"]


class ListAgentsFoodAPIView(generics.ListAPIView):

    serializer_class = FoodSerializer
    pagination_class = FoodPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = FoodFilter
    search_fields = ["country", "city"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        user = self.request.user
        queryset = Food.objects.filter(user=user).order_by("-created_at")
        return queryset


class FoodViewsAPIView(generics.ListAPIView):
    serializer_class = FoodViewSerializer
    queryset = FoodViews.objects.all()


class FoodDetailView(APIView):
    def get(self, request, slug):
        food = Food.objects.get(slug=slug)

        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        if not FoodViews.objects.filter(food=food, ip=ip).exists():
            FoodViews.objects.create(food=food, ip=ip)

            food.views += 1
            property.save()

        serializer = FoodSerializer(food, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def update_food_api_view(request, slug):
    try:
        food = Food.objects.get(slug=slug)
    except Food.DoesNotExist:
        raise FoodNotFound

    user = request.user
    if food.user != user:
        return Response(
            {"error": "You can't update or edit a item that doesn't belong to you"},
            status=status.HTTP_403_FORBIDDEN,
        )
    if request.method == "PUT":
        data = request.data
        serializer = FoodSerializer(food, data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_food_api_view(request):
    user = request.user
    data = request.data
    data["user"] = request.user.pkid
    serializer = FoodCreateSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        logger.info(
            f"food {serializer.data.get('title')} created by {user.username}"
        )
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_food_api_view(request, slug):
    try:
        food = Food.objects.get(slug=slug)
    except Food.DoesNotExist:
        raise FoodNotFound

    user = request.user
    if food.user != user:
        return Response(
            {"error": "You can't delete a item that doesn't belong to you"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "DELETE":
        delete_operation = food.delete()
        data = {}
        if delete_operation:
            data["success"] = "Deletion was successful"
        else:
            data["failure"] = "Deletion failed"
        return Response(data=data)


@api_view(["POST"])
def uploadFoodImage(request):
    data = request.data

    food_id = data["food_id"]
    food = Food.objects.get(id=food_id)
    food.cover_photo = request.FILES.get("cover_photo")
    food.photo1 = request.FILES.get("photo1")
    food.photo2 = request.FILES.get("photo2")
    food.photo3 = request.FILES.get("photo3")
    food.photo4 = request.FILES.get("photo4")
    food.save()
    return Response("Image(s) uploaded")


class FoodSearchAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = FoodCreateSerializer

    def post(self, request):
        queryset = Food.objects.filter(published_status=True)
        data = self.request.data

       

        catch_phrase = data["catch_phrase"]
        queryset = queryset.filter(description__icontains=catch_phrase)

        serializer = FoodSerializer(queryset, many=True)

        return Response(serializer.data)
