from core.models import ExpenseType, Expense, VoucherFile

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


class VoucherFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherFile
        fields = ("file_url", "file_id", "file_type")


class ExpenseSerializer(serializers.ModelSerializer):
    voucher_file = VoucherFileSerializer(read_only=True)
    voucher_file_id = serializers.CharField(write_only=True, allow_null=True)
    voucher_file_url = serializers.URLField(write_only=True, allow_null=True)
    voucher_file_type = serializers.ChoiceField(
        write_only=True, allow_null=True, choices=VoucherFile.FILE_TYPE_CHOICES
    )
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
            "voucher_file",
            "voucher_file_url",
            "voucher_file_id",
            "voucher_file_type",
        )
        read_only_fields = ("total_price",)

    def validate(self, data):
        if (
            ("voucher_file_id" in data and "voucher_file_url" not in data)
            or ("voucher_file_url" in data and "voucher_file_id" not in data)
            or (data.get("voucher_file_id") is None and data.get("voucher_file_url") is not None)
            or (data.get("voucher_file_id") is not None and data.get("voucher_file_url") is None)
        ):
            raise serializers.ValidationError("The Voucher File needs both, id and URL.")

        return data

    def create(self, validated_data):
        voucher_file = None
        if "voucher_file_id" in validated_data and "voucher_file_url" in validated_data:
            voucher_file_id = validated_data.pop("voucher_file_id")
            voucher_file_url = validated_data.pop("voucher_file_url")
            voucher_file_type = validated_data.pop("voucher_file_type")
            voucher_file = VoucherFile.objects.create(
                file_id=voucher_file_id,
                file_url=voucher_file_url,
                file_type=voucher_file_type,
                owner=validated_data["owner"],
            )

        expense = Expense.objects.create(voucher_file=voucher_file, **validated_data)

        return expense

    def update(self, instance, validated_data):
        if "voucher_file_id" in validated_data and "voucher_file_url" in validated_data:
            voucher_file_id = validated_data.pop("voucher_file_id")
            voucher_file_url = validated_data.pop("voucher_file_url")
            voucher_file_type = validated_data.pop("voucher_file_type")

            if instance.voucher_file:
                voucher_file = VoucherFile.objects.get(file_id=instance.voucher_file.file_id)
                if voucher_file_id is None:
                    instance.voucher_file = None
                    voucher_file.delete()
                elif instance.voucher_file.file_id != voucher_file_id:
                    voucher_file.delete()
                    instance.voucher_file = VoucherFile.objects.create(
                        file_id=voucher_file_id, file_url=voucher_file_url, owner=instance.owner
                    )
                elif instance.voucher_file.file_url != voucher_file_url:
                    voucher_file.file_url = voucher_file_url
                    voucher_file.file_type = voucher_file_type
                    voucher_file.save()
            else:
                if voucher_file_id is not None:
                    instance.voucher_file = VoucherFile.objects.create(
                        file_id=voucher_file_id,
                        file_url=voucher_file_url,
                        file_type=voucher_file_type,
                        owner=instance.owner,
                    )

            instance.save()

        super().update(instance, validated_data)
        return instance
