from django.contrib import admin

from commons.admin import GenericNameCodeAdmin
from inventory import models


class TransferRecordAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'transfer_type', 'originating_unit', 'receiving_unit')
    autocomplete_fields = ('transfer_type', 'originating_unit', 'receiving_unit')
    readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')
    ordering = ('date', )

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user

        obj.updated_by = request.user
        obj.save()


admin.site.register(models.TransferRecord, TransferRecordAdmin)
admin.site.register(models.TransferType, GenericNameCodeAdmin)
admin.site.register(models.TransferStatus, GenericNameCodeAdmin)
