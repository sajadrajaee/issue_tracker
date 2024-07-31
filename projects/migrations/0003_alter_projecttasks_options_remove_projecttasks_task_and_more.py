# Generated by Django 5.0.7 on 2024-07-30 23:24

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_remove_project_project_doer_projecttasks'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projecttasks',
            options={'verbose_name': "project's tasks", 'verbose_name_plural': "project's tasks"},
        ),
        migrations.RemoveField(
            model_name='projecttasks',
            name='task',
        ),
        migrations.AddField(
            model_name='projecttasks',
            name='content',
            field=models.CharField(default=None, max_length=300),
        ),
        migrations.AddField(
            model_name='projecttasks',
            name='title',
            field=models.CharField(default=django.utils.timezone.now, max_length=59),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projecttasks',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='assigned to'),
        ),
    ]
