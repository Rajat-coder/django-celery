from django.contrib import admin
from authentication.models import User
from import_export.admin import ImportExportModelAdmin
from shared.views import *
from authentication.tasks import *

# Register your models here.


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    list_per_page=1000
    list_display=("username","email")
    actions=("export_csv",
    )

    download_as_csv_fields = (
    'first_name', 'last_name', 'username',)

    def export_csv(self, request, queryset):
        user_id_list = queryset.values_list("id", flat = True)
        user_id_list = list(user_id_list)
        user_email = request.user.email
        download_as_csv_task.delay(user_email , user_id_list)

