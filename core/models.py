from django.contrib.auth.models import User
from django.db import models


class AutoTimestamps(models.Model):
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        abstract = True


class ExpenseType(AutoTimestamps):
    name = models.CharField("Name", max_length=255)
    description = models.TextField("Description", blank=True, null=True)

    class Meta:
        verbose_name = "Expense Type"
        verbose_name_plural = "Expense Types"

    def __str__(self):
        return self.name


class VoucherFile(AutoTimestamps):
    PDF = "PDF"
    IMAGE = "IMAGE"
    FILE_TYPE_CHOICES = ((PDF, "PDF"), (IMAGE, "IMAGE"))

    file_id = models.CharField("File Id", max_length=255, unique=True, primary_key=True)
    file_url = models.URLField("File URL")
    file_type = models.CharField("File Type", choices=FILE_TYPE_CHOICES, default=IMAGE)
    owner = models.ForeignKey(User, verbose_name="Owner", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Voucher File"
        verbose_name_plural = "Voucher Files"

    def __str__(self):
        return self.file_id


class Expense(AutoTimestamps):
    description = models.TextField("Description", blank=True, null=True)
    unit_price = models.DecimalField("Unit Price", max_digits=10, decimal_places=2)
    quantity = models.DecimalField("Quantity", max_digits=10, decimal_places=2)
    shipping_price = models.DecimalField("Shipping Price", max_digits=10, decimal_places=2)
    type = models.ForeignKey(ExpenseType, verbose_name="Expense Type", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, verbose_name="Owner", on_delete=models.CASCADE)
    voucher_file = models.ForeignKey(
        VoucherFile, verbose_name="Voucher File", on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"

    def __str__(self):
        return f"{self.description} - {self.owner.username}"

    @property
    def total_price(self):
        return (self.unit_price * self.quantity) + self.shipping_price
