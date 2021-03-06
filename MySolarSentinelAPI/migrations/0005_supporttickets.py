# Generated by Django 3.0.8 on 2020-08-17 04:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MySolarSentinelAPI', '0004_auto_20200816_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportTickets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TicketOpenDate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='ticket created date')),
                ('TicketStatus', models.CharField(default='Create', max_length=10)),
                ('CustomerAcknowledged', models.BooleanField(default=False, verbose_name='CustomerAcknowledged')),
                ('TechnicianName', models.CharField(blank=True, max_length=10, null=True)),
                ('Notes', models.CharField(blank=True, max_length=1024, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='MySolarSentinelAPI.Customer', verbose_name='customer')),
            ],
        ),
    ]
