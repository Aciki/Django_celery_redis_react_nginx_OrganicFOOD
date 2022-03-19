from django.urls import path

from . import views

urlpatterns = [
    path("all/", views.ListAllFoodAPIView.as_view(), name="all-items"),
    path(
        "agents/", views.ListAgentsFoodAPIView.as_view(), name="agent-items"
    ),
    path("create/", views.create_food_api_view, name="item-create"),
    path(
        "details/<slug:slug>/",
        views.FoodDetailView.as_view(),
        name="food-details",
    ),
    path("update/<slug:slug>/", views.update_food_api_view, name="update-food"),
    path("delete/<slug:slug>/", views.delete_food_api_view, name="delete-foood"),
    path("search/", views.FoodSearchAPIView.as_view(), name="food-search"),
]
