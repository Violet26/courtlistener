# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people_db', '0005_auto_20160318_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='cl_id',
            field=models.CharField(help_text='A unique identifier for judge, also indicating source of data.', max_length=30, unique=True, null=True, db_index=True),
        ),
    ]
