from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "zillow"

router = DefaultRouter()
router.register("zillow", views.ZillowView)

urlpatterns = [path("", include(router.urls))]
