from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("supersecret/", admin.site.urls),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("djoser.urls.jwt")),
    path("api/v1/profile/", include("apps.profiles.urls")),
    path("api/v1/properties/", include("apps.food.urls")),
    path("api/v1/ratings/", include("apps.ratings.urls")),
    path("api/v1/enquiries/", include("apps.enquries.urls")),
]


admin.site.site_header = "Organic Food Admin"
admin.site.site_title = "Organic FooD Admin Portal"
admin.site.index_title = "Welcome to the Organic Food Portal"
