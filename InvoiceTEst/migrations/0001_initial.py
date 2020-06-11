# Generated by Django 3.0.7 on 2020-06-11 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_to_import', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceHead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=70, unique=True)),
                ('tax_payer_id', models.CharField(blank=True, max_length=30, null=True)),
                ('VAT_code', models.CharField(max_length=2)),
                ('supplier_name', models.CharField(max_length=70)),
                ('country_code', models.CharField(max_length=3)),
                ('county_code', models.CharField(max_length=2)),
                ('postal_code', models.CharField(max_length=6)),
                ('city', models.CharField(max_length=70)),
                ('public_place_category', models.CharField(max_length=30)),
                ('number', models.IntegerField()),
                ('floor', models.IntegerField()),
                ('door', models.IntegerField()),
                ('supplier_bank_account_number', models.CharField(max_length=30)),
                ('customer_name', models.CharField(max_length=60)),
                ('invoice_category', models.CharField(max_length=12)),
                ('invoice_delivery_date', models.DateTimeField()),
                ('small_business_indicator', models.CharField(max_length=6)),
                ('currency_code', models.CharField(max_length=3)),
                ('exchange_rate', models.CharField(max_length=3)),
                ('payment_method', models.CharField(max_length=12)),
                ('payment_date', models.DateTimeField()),
                ('invoice_appearance', models.CharField(max_length=20)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InvoiceTEst.Invoice')),
            ],
        ),
    ]
