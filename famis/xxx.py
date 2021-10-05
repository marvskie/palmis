# def facility_count(self, obj):
    #     return obj.facility_info.count()
    # facility_count.short_description = "Number of Facility"
    # facility_count.admin_order_field = "facility_info"

    # def get_queryset(self, request):
    #     qs = super(InventoryAdmin, self).get_queryset(request)
    #     return qs.annotate(facility_count=Count('facility_info'))

    # def facility_count(self, inst):
    #     return inst.facility_count
    
    # facility_count.short_description = "Number of Facility"
    # facility_count.admin_order_field = "facility_info"