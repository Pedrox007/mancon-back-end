from django.contrib import admin

from core.models import Expense, ExpenseType


@admin.register(ExpenseType)
class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


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
        "owner",
    )
    search_fields = ("description", "owner__username")
    list_filter = ("type", "owner")
