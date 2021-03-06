# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donate', '0004_monthly_donations'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlydonation',
            name='failure_count',
            field=models.SmallIntegerField(default=0, help_text='The number of times this customer ID has failed. If a threshold is exceeded, we disable the subscription.'),
        ),
    ]
