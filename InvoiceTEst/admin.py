from django.contrib import admin

from InvoiceTEst.models import InvoiceHead, Invoice

admin.site.register(Invoice)
admin.site.register(InvoiceHead)