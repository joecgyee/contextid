# attributes/migrations/0004_repopulate_and_remap.py
from django.db import migrations

def repopulate_fixed_data(apps, schema_editor):
    PriorityRule = apps.get_model('attributes', 'PriorityRule')
    ValueType = apps.get_model('attributes', 'ValueType')

    # Repopulate Priority Rules
    for name in ['DEFAULT', 'OVERRIDE', 'FALLBACK']:
        PriorityRule.objects.get_or_create(name=name)

    # Repopulate Value Types
    for name in ['STRING', 'DATE', 'INT', 'URL', 'BOOLEAN']:
        ValueType.objects.get_or_create(name=name)

def remap_value_type_fk(apps, schema_editor):
    ProfileAttribute = apps.get_model('attributes', 'ProfileAttribute')
    ValueType = apps.get_model('attributes', 'ValueType')

    # Build a lookup dict {name: id}
    vt_lookup = {vt.name: vt.id for vt in ValueType.objects.all()}

    for pa in ProfileAttribute.objects.all():
        if pa.value_type_id:
            # Instead of pa.value_type.name, use pa.value_type_id or store old name separately
            # Assuming your old data had names like 'STRING', 'DATE', etc.
            old_name = pa.value_type  # careful: historical model may store the raw value
            if isinstance(old_name, str):
                name = old_name
            else:
                # fallback: if pa.value_type is a related object, get its name
                try:
                    name = old_name.name
                except AttributeError:
                    continue

            if name in vt_lookup:
                pa.value_type_id = vt_lookup[name]
                pa.save(update_fields=['value_type_id'])

class Migration(migrations.Migration):

    dependencies = [
        ('attributes', '0003_priorityrule_valuetype_and_more'),
    ]

    operations = [
        migrations.RunPython(repopulate_fixed_data),
        migrations.RunPython(remap_value_type_fk),
    ]