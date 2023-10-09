from django.db import migrations


def create_default_expense_types(apps, schema_editor):
    expense_type_model = apps.get_model("core", "ExpenseType")

    expense_types = [
        expense_type_model(name="Alvenaria"),
        expense_type_model(name="Elétrica/Dados"),
        expense_type_model(name="Hidráulica"),
        expense_type_model(name="Mão de Obra"),
        expense_type_model(name="Acabamento"),
        expense_type_model(name="Equipamentos"),
    ]

    expense_type_model.objects.bulk_create(expense_types)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_expense_types),
    ]
