# Generated by Django 5.1.4 on 2024-12-04 16:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_subject_contents_alter_content_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='subject',
        ),
        migrations.AddField(
            model_name='content',
            name='classroom',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='app.classroom'),
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
    ]
