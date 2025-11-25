from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Hospital, Disease, District, Patient, Rate





class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        'username', 'email', 'is_client', 'is_admin', 'date_joined'
    )
    list_filter = ('is_client', 'is_admin')
    search_fields = ('username', 'email')
    ordering = ('id',)

    fieldsets = (
        ('Login Info', {
            'fields': ('username', 'password')
        }),
        ('Personal Details', {
            'fields': ('first_name', 'last_name', 'email', 'image')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_client', 'is_admin',
                'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Extra Info', {
            'fields': ('date_joined',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'is_client', 'is_admin'
            )
        }),
    )




@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'phone', 'website')
    search_fields = ('name', 'location')
    list_filter = ('location',)




@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('hospitals',)




@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)




@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'district', 'disease', 'surgery', 'contact', 'blood_group', 'inqury_date')
    search_fields = ('name', 'contact', 'location')
    list_filter = ('district', 'disease', 'surgery', 'blood_group')




@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ('user', 'hospital', 'rating')
    list_filter = ('rating', 'hospital')
    search_fields = ('user__username', 'hospital__name')




admin.site.register(User, UserAdmin)

