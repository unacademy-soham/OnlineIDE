from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("user", views.UserViewSet)
router.register("submit", views.SubmissionsViewSet)

urlpatterns = [
    path("", views.hello_world)
]

urlpatterns += router.urls