from django.contrib import admin

from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from exec import models

class FileCommentInline(admin.TabularInline):
    model = models.FileComment
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('branch','name',)
    search_fields = ('name',)
    ordering = ('name', )

class FileAttachmentAdmin(admin.ModelAdmin):
    list_display = ('title','file','branch','category','uploaded_by','created_at', 'updated_at',)
    search_fields = ('title',)
    list_filter = ('title', 'branch', 'category',)
    ordering = ('updated_at', )
    inlines = [FileCommentInline]



# class FileCommentAdmin(admin.ModelAdmin):
#     list_display = ('created_by','text','created_at', 'updated_at',)
#     search_fields = ('text',)
#     ordering = ('updated_at', )

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','branch','description','location','start_time', 'end_time','due_date', 'created_by', 'updated_at')
    search_fields = ('branch','description','location','due_date', 'created_by',)
    list_filter = ('branch','description','location','due_date', 'created_by',)
    ordering = ('updated_at', )

# Register your models here.
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.FileAttachment, FileAttachmentAdmin)
admin.site.register(models.Task, TaskAdmin)


# ============= admin log 


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'user__account__role__organization',
        'content_type',
        'action_flag'

    ]

    search_fields = [
        'object_repr',
        'change_message',
        'user__account__role__organization',

    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"