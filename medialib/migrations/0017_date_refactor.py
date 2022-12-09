from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medialib', '0016_platform_bootstrap_icon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='Media',
            old_name='created_date',
            new_name='date',
        ),
    ]
