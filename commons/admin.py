from django.contrib import admin

from commons.models import Serviceability, AcquisitionMode, Pamu, Unit,  ProcurementMode, Fssu, \
    Organization, Role, Account, Region, Branch
from mobility.models import VehicleRecord


class GenericNameCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('code', )


class VehicleRecordTabular(admin.TabularInline):
    model = VehicleRecord
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class AcquisitionAdmin(admin.ModelAdmin):
    inlines = [VehicleRecordTabular]
    search_fields = ('name', )
    ordering = ('name', )


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'mother_unit', 'pamu', 'alt_pamu')
    list_filter = ('pamu', )
    search_fields = ('name', )
    ordering = ('name', )


class ProcurementModeAdmin(admin.ModelAdmin):
    fields = ('name', 'full_name', 'code', 'order')
    list_display = ('full_name', 'code', 'order')
    search_fields = ('full_name', )
    ordering = ('order', )


class RoleInline(admin.TabularInline):
    model = Role
    extra = 0


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    inlines = (RoleInline, )


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', )
    search_fields = ('name', 'organization__name')

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'role', 'division', 'active', 'bypass_otp', 'require_change_pw')
    readonly_fields = ('name', 'created_by', 'created_at', 'updated_by', 'updated_at', )
    search_fields = ('user__username', 'name')
    list_filter = ('role__organization', 'active', 'bypass_otp')
    list_editable = ('active', 'bypass_otp', 'require_change_pw')
    autocomplete_fields = ('user', 'role',)
    ordering = ('user', )

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user

        obj.updated_by = request.user

        super().save_model(request, obj, form, change)

        obj.user.first_name = obj.first_name
        obj.user.last_name = obj.last_name
        obj.user.email = obj.email or ''
        obj.user.active = obj.active
        obj.user.save()


admin.site.register(Account, AccountAdmin)
admin.site.register(AcquisitionMode, AcquisitionAdmin)
admin.site.register(ProcurementMode, ProcurementModeAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Fssu, GenericNameCodeAdmin)
admin.site.register(Pamu, GenericNameCodeAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register([Serviceability, Region, Branch])
admin.site.register(Role, RoleAdmin)
