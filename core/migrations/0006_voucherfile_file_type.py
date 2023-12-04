# Generated by Django 4.2.7 on 2023-12-02 18:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_remove_expense_voucher_file_url_voucherfile_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="voucherfile",
            name="file_type",
            field=models.CharField(
                choices=[("PDF", "PDF"), ("IMAGE", "IMAGE")], default="IMAGE", verbose_name="File Type"
            ),
        ),
    ]
