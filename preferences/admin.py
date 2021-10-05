from django.contrib import admin
from preferences.models import SystemPreference


class SystemPreferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', )
    fields = ('name', 'description', 'code', 'val_type', 'value')
    search_fields = ('name', 'description')

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj and obj.id:
            try:
                return readonly_fields + ('val_type', )
            except TypeError:
                pass
        return readonly_fields

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)

        if instance.val_type == SystemPreference.TYPE_BOOLEAN:
            instance.remarks = '1 - True: 0 - False'

        return super().save_model(request, obj, form, change)


admin.site.register(SystemPreference, SystemPreferenceAdmin)
