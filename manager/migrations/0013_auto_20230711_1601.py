from django.db import migrations


def load_fixture(apps, schema_editor):
    from django.core.management import call_command
    call_command("loaddata", "fixture_data.json")


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0012_alter_project_status"),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_func)
    ]
