from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("user", views.UserViewSet)
router.register("submit", views.SubmissionsViewSet)

urlpatterns = [
    path("", views.hello_world),
    path("login/", views.LoginView.as_view()),
    path("register/", views.register),
    path("thumbnail", views.create_thumbnail)
]

urlpatterns += router.urls