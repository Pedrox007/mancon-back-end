from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core import views

router = DefaultRouter()

router.register("expense-types", views.ExpenseTypeViewSet)
router.register("expenses", views.ExpenseViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
