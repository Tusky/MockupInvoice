from xml.etree.ElementTree import ElementTree, fromstring

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

STATUS_CHOICES = (
    (0, 'Parsing'),
    (1, 'Invalid'),
    (2, 'Parsed')
)


class Invoice(models.Model):
    file_to_import = models.FileField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)


class InvoiceHead(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=70, unique=True)
    tax_payer_id = models.CharField(max_length=30, null=True, blank=True)
    VAT_code = models.CharField(max_length=2, null=True, blank=True)
    supplier_name = models.CharField(max_length=70, null=True, blank=True)
    country_code = models.CharField(max_length=3, null=True, blank=True)
    county_code = models.CharField(max_length=2, null=True, blank=True)
    postal_code = models.CharField(max_length=6, null=True, blank=True)
    street_name = models.CharField(max_length=70, null=True, blank=True)
    city = models.CharField(max_length=70, null=True, blank=True)
    public_place_category = models.CharField(max_length=30, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    floor = models.IntegerField(null=True, blank=True)
    door = models.IntegerField(null=True, blank=True)
    supplier_bank_account_number = models.CharField(max_length=30, null=True, blank=True)
    customer_name = models.CharField(max_length=60, null=True, blank=True)
    invoice_category = models.CharField(max_length=12, null=True, blank=True)
    invoice_delivery_date = models.DateField(null=True, blank=True)
    small_business_indicator = models.BooleanField(default=False)
    currency_code = models.CharField(max_length=3, null=True, blank=True)
    exchange_rate = models.CharField(max_length=3, null=True, blank=True)
    payment_method = models.CharField(max_length=12, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    invoice_appearance = models.CharField(max_length=20, null=True, blank=True)


@receiver(post_save, sender=Invoice)
def import_file(instance: Invoice, **kwargs):
    with open(instance.file_to_import.path) as fp:
        tree = ElementTree(fromstring(fp.read()))
        invoice_main = tree.find('invoiceMain')
        invoice = invoice_main.find('invoice')
        invoice_head = invoice.find('invoiceHead')
        supplier_info = invoice_head.find('supplierInfo')
        supplier_tax_number = supplier_info.find('supplierTaxNumber')
        supplier_address = supplier_info.find('supplierAddress')
        detailed_address = supplier_address.find('detailedAddress')
        customer_info = invoice_head.find('customerInfo')
        invoice_detail = invoice_head.find('invoiceDetail')
        invoice_head_obj = InvoiceHead(
            invoice=instance,
            invoice_number=tree.find('invoiceNumber').text,
            tax_payer_id=supplier_tax_number.find('taxpayerId').text,
            VAT_code=supplier_tax_number.find('vatCode').text,
            county_code=supplier_tax_number.find('countyCode').text,
            supplier_name=supplier_info.find('supplierName').text,
            country_code=detailed_address.find('countryCode').text,
            postal_code=detailed_address.find('postalCode').text,
            city=detailed_address.find('city').text,
            street_name=detailed_address.find('streetName').text,
            public_place_category=detailed_address.find('publicPlaceCategory').text,
            number=int(detailed_address.find('number').text.replace('.', '')),
            floor=int(detailed_address.find('floor').text.replace('.', '')),
            door=int(detailed_address.find('door').text.replace('.', '')),
            supplier_bank_account_number=supplier_info.find('supplierBankAccountNumber').text,
            customer_name=customer_info.find('customerName').text,
            invoice_category=invoice_detail.find('invoiceCategory').text,
            invoice_delivery_date=invoice_detail.find('invoiceDeliveryDate').text,
            small_business_indicator=invoice_detail.find('smallBusinessIndicator').text == 'true',
            exchange_rate=invoice_detail.find('exchangeRate').text,
            payment_method=invoice_detail.find('paymentMethod').text,
            payment_date=invoice_detail.find('paymentDate').text,
            invoice_appearance=invoice_detail.find('invoiceAppearance').text
        )
        invoice_head_obj.save()
