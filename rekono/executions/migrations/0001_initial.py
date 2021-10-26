# Generated by Django 3.2.7 on 2021-10-23 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Execution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rq_job_id', models.TextField(blank=True, max_length=50, null=True)),
                ('rq_job_pid', models.IntegerField(blank=True, null=True)),
                ('output_file', models.TextField(blank=True, max_length=50, null=True)),
                ('output_plain', models.TextField(blank=True, null=True)),
                ('output_error', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Requested'), (2, 'Skipped'), (3, 'Running'), (4, 'Cancelled'), (5, 'Error'), (6, 'Completed')], default=1)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
