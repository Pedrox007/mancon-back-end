from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, views
from rest_framework.response import Response

from core.filters import ExpenseFilter
from core.models import ExpenseType, Expense
from core.serializers import ExpenseTypeSerializer, ExpenseSerializer, UserSerializer


class ExpenseTypeViewSet(viewsets.ModelViewSet):
    queryset = ExpenseType.objects.all()
    serializer_class = ExpenseTypeSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filterset_class = ExpenseFilter


class UserViewSet(views.APIView):
    def get(self, request):
        user = request.user

        return Response(UserSerializer(user).data)

    @extend_schema(
        request=UserSerializer,
        responses={200: UserSerializer},
    )
    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
