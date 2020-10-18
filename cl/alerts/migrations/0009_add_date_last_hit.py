# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0008_add_docket_alerts'),
    ]

    operations = [
        migrations.AddField(
            model_name='docketalert',
            name='date_last_hit',
            field=models.DateTimeField(null=True, verbose_name='time of last trigger', blank=True),
        ),
    ]
