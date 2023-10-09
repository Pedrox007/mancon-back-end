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
            "owner",
            "owner_id",
        )
        read_only_fields = ("total_price",)

    def create(self, validated_data):
        owner = validated_data.pop("owner_id")
        expense = Expense.objects.create(**validated_data, owner=owner)

        return expense

    def update(self, instance, validated_data):
        instance.description = validated_data.get("description", instance.description)
        instance.unit_price = validated_data.get("unit_price", instance.unit_price)
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.shipping_price = validated_data.get("shipping_price", instance.shipping_price)
        instance.type = validated_data.get("type", instance.type)
        instance.save()

        return instance
