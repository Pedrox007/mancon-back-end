from core.models import ExpenseType, Expense

from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class ExpenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseType
        fields = ("id", "name", "description")


class ExpenseSerializer(serializers.ModelSerializer):
    type = ExpenseTypeSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(queryset=ExpenseType.objects.all(), source="type", write_only=True)
    owner = UserSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="owner", write_only=True)

    class Meta:
        model = Expense
        fields = (
            "id",
            "description",
            "total_price",
            "unit_price",
            "quantity",
            "shipping_price",
            "type",
            "type_id",
            "owner",
            "owner_id",
        )
        read_only_fields = ("total_price",)
