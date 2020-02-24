"""
Custom migration for adding periodic tasks
"""
from datetime import datetime

from django.db import migrations


def create_periodic_tasks(apps, schema_editor):
    """
    Add periodic tasks to update exchange rates of currencies every day
    """
    db_alias = schema_editor.connection.alias
    CrontabSchedule = apps.get_model("django_celery_beat", "CrontabSchedule")
    crontab_schedule = CrontabSchedule.objects.using(db_alias).create(
        minute='30',
        hour='12'
    )
    PeriodicTask = apps.get_model("django_celery_beat", "PeriodicTask")
    PeriodicTask.objects.using(db_alias).create(
        name='Update exchange rates for the currencies',
        task='currency_converter.currencies.tasks.update_exchange_rates',
        crontab=crontab_schedule,
        description='Update exchange rates for the currencies every day at 12:30 pm UTC',
        start_time=datetime.now()
    )
    # Add a period task to load values when initializing the project
    IntervalSchedule = apps.get_model("django_celery_beat", "IntervalSchedule")
    interval = IntervalSchedule.objects.using(db_alias).create(
        every=1,
        period='seconds'
    )
    PeriodicTask.objects.using(db_alias).create(
        name='Load exchange rates for the currencies',
        task='currency_converter.currencies.tasks.update_exchange_rates',
        description='Load exchange rates for the currencies',
        start_time=datetime.now(),
        interval=interval,
        one_off=True  # perform it only once
    )


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0002_add_restrictions'),
        ('django_celery_beat', '0012_periodictask_expire_seconds')
    ]

    operations = [
        migrations.RunPython(create_periodic_tasks)
    ]
