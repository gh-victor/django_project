from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomUserResource(resources.ModelResource):
    class Meta:
        model = User


@admin.register(User)
class CustomUserAdmin(ImportExportModelAdmin):
    list_display = ('email', 'is_superuser', 'is_staff', 'is_active')
    list_filter = ('is_superuser', 'is_staff')
    ordering = ['id']

    resource_class = CustomUserResource