from django.contrib import admin

from core.models import Expense, ExpenseType, VoucherFile


@admin.register(ExpenseType)
class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(VoucherFile)
class VoucherFileAdmin(admin.ModelAdmin):
    list_display = ("file_id", "file_url", "file_type", "owner")
    search_fields = ("file_id",)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "description",
        "total_price",
        "unit_price",
        "quantity",
        "shipping_price",
        "type",
        "voucher_file",
        "owner",
    )
    search_fields = ("description", "owner__username")
    list_filter = ("type", "owner")
