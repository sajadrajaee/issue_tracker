# Generated by Django 5.0.7 on 2024-07-30 22:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='project_doer',
        ),
        migrations.CreateModel(
            name='ProjectTasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=250)),
                ('time_to_finish', models.DateField(default=None, verbose_name='time to finish')),
                ('task_status', models.CharField(choices=[('free', 'free'), ('working_on', 'working on'), ('done', 'done')], max_length=10)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='assigned to')),
            ],
        ),
    ]
