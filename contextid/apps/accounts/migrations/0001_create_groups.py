from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    def get_perms(app_label, model_name, actions=['add', 'change', 'delete', 'view']):
        perms = []
        for action in actions:
            codename = f"{action}_{model_name}"
            # Using .filter().first() is safer in migrations to avoid crashes
            p = Permission.objects.filter(content_type__app_label=app_label, codename=codename).first()
            if p:
                perms.append(p)
        return perms

    # Create Admins
    admin_group, _ = Group.objects.get_or_create(name='Admins')
    admin_group.permissions.set(
        get_perms('admin', 'logentry', ['add', 'view']) +
        get_perms('attributes', 'attributecontextrule') +
        get_perms('attributes', 'priorityrule') +
        get_perms('attributes', 'profileattribute') +
        get_perms('attributes', 'valuetype') +
        get_perms('auth', 'user', ['add', 'view']) +        
        get_perms('contexts', 'context', ['add', 'change', 'view']) +
        get_perms('profiles', 'identityprofile')
    )

    # Create Users
    user_group, _ = Group.objects.get_or_create(name='Users')
    user_group.permissions.set(
        get_perms('attributes', 'attributecontextrule', ['view']) +
        get_perms('attributes', 'priorityrule', ['view']) +
        get_perms('attributes', 'profileattribute') +
        get_perms('attributes', 'valuetype', ['view']) +
        get_perms('contexts', 'context', ['view']) +
        get_perms('profiles', 'identityprofile')
    )

def remove_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Admins', 'Users']).delete()

class Migration(migrations.Migration):
    # This migration is the FIRST for the accounts app
    initial = True 

    dependencies = [
        # Depend on built-in Auth models
        ('auth', '__latest__'),
        ('contenttypes', '__latest__'),
        # Depend on your other apps' initial migrations
        ('profiles', '0001_initial'),
        ('attributes', '0001_initial'),
        ('contexts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups, remove_groups),
    ]