from rest_framework import viewsets

from core.filters import ExpenseFilter
from core.models import ExpenseType, Expense
from core.serializers import ExpenseTypeSerializer, ExpenseSerializer


class ExpenseTypeViewSet(viewsets.ModelViewSet):
    queryset = ExpenseType.objects.all()
    serializer_class = ExpenseTypeSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filterset_class = ExpenseFilter
