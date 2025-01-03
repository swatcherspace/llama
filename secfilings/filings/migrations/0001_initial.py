# Generated by Django 4.2.17 on 2024-12-24 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cik', models.CharField(max_length=20)),
                ('company', models.CharField(max_length=255)),
                ('filing_type', models.CharField(max_length=50)),
                ('filing_date', models.DateField()),
                ('period_of_report', models.DateField()),
                ('sic', models.CharField(max_length=10)),
                ('state_of_inc', models.CharField(max_length=2)),
                ('state_location', models.CharField(max_length=100)),
                ('fiscal_year_end', models.CharField(max_length=4)),
                ('filing_html_index', models.URLField()),
                ('htm_filing_link', models.URLField()),
                ('complete_text_filing_link', models.URLField()),
                ('filename', models.CharField(max_length=255)),
                ('item_1', models.TextField(blank=True, null=True)),
                ('item_2', models.TextField(blank=True, null=True)),
                ('item_3', models.TextField(blank=True, null=True)),
                ('item_4', models.TextField(blank=True, null=True)),
                ('item_5', models.TextField(blank=True, null=True)),
                ('item_6', models.TextField(blank=True, null=True)),
                ('item_7', models.TextField(blank=True, null=True)),
                ('item_8', models.TextField(blank=True, null=True)),
                ('item_9', models.TextField(blank=True, null=True)),
                ('item_10', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
