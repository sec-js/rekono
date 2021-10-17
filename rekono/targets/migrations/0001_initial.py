# Generated by Django 3.2.7 on 2021-10-17 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.TextField(max_length=100)),
                ('type', models.IntegerField(choices=[(1, 'Private Ip'), (2, 'Public Ip'), (3, 'Network'), (4, 'Ip Range'), (5, 'Domain')])),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='targets', to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='TargetPort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port', models.IntegerField()),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_ports', to='targets.target')),
            ],
        ),
        migrations.AddConstraint(
            model_name='targetport',
            constraint=models.UniqueConstraint(fields=('target', 'port'), name='unique target port'),
        ),
        migrations.AddConstraint(
            model_name='target',
            constraint=models.UniqueConstraint(fields=('project', 'target'), name='unique target'),
        ),
    ]
