# Generated by Django 3.2.7 on 2021-09-25 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tools', '0001_initial'),
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('processes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intensity', models.IntegerField(blank=True, choices=[(1, 'Sneaky'), (2, 'Low'), (3, 'Normal'), (4, 'Hard'), (5, 'Insane')], default=3, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Requested'), (2, 'Skipped'), (3, 'Running'), (4, 'Cancelled'), (5, 'Error'), (6, 'Completed')], default=1)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('configuration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tools.configuration')),
                ('executor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('process', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='processes.process')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='projects.target')),
                ('tool', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tools.tool')),
            ],
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.IntegerField(choices=[(1, 'Technology'), (2, 'Version'), (3, 'Http Endpoint'), (4, 'Cve'), (5, 'Exploit'), (6, 'Wordlist')])),
                ('value', models.TextField(max_length=250)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameters', to='executions.request')),
            ],
        ),
        migrations.CreateModel(
            name='Execution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('output_file', models.TextField(blank=True, max_length=50, null=True)),
                ('output_plain', models.TextField(blank=True, null=True)),
                ('output_error', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Requested'), (2, 'Skipped'), (3, 'Running'), (4, 'Cancelled'), (5, 'Error'), (6, 'Completed')], default=1)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='executions', to='executions.request')),
                ('step', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='processes.step')),
            ],
        ),
    ]
