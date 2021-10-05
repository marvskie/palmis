from django.contrib import admin

from message.models import Message


class MessageAdmin(admin.ModelAdmin):
    search_fields = ('remarks', )
    list_filter = ('content_type', )
    readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')
    ordering = ('-created_at', )

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user

        obj.updated_by = request.user

        super().save_model(request, obj, form, change)


# admin.site.register(Message, MessageAdmin)
