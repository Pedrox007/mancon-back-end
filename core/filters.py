from django_filters import rest_framework as filters

from core.models import Expense


class ExpenseFilter(filters.FilterSet):
    class Meta:
        model = Expense
        fields = {
            "type_id": ["exact", "in"],
            "owner_id": ["exact", "in"],
            "created_at": ["exact", "in", "gt", "gte", "lt", "lte"],
            "updated_at": ["exact", "in", "gt", "gte", "lt", "lte"],
        }
