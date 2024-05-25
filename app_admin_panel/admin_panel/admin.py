from django.contrib import admin
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from import_export.resources import ModelResource
from admin_panel.models import User, SupportRequest, Dispatcher, Post, MailingLog, Card


class CustomImportExport(ImportExportModelAdmin, ExportActionModelAdmin):
    pass


# setup import
class UserResource(ModelResource):
    class Meta:
        model = User
        import_id_fields = ('user_id',)


@admin.register(User)
class UserAdmin(CustomImportExport):
    resource_classes = [UserResource]
    list_display = ('user_id', 'first_name', 'created_at', 'is_registered_meditation', 'is_registered_days')
    list_display_links = ('user_id', 'first_name',)
    list_editable = ('is_registered_meditation', 'is_registered_days')
    list_filter = ('is_registered_meditation', 'is_registered_days')

@admin.register(SupportRequest)
class SupportRequestAdmin(CustomImportExport):
    list_display = [field.name for field in SupportRequest._meta.fields]


@admin.register(Dispatcher)
class OrderAdmin(CustomImportExport):
    exclude = ('is_bg', )
    list_display = [field.name for field in Dispatcher._meta.fields if field.name != 'is_bg']
    list_editable = ('is_registered_meditation', 'is_registered_days', 'is_for_all_users')


@admin.register(Post)
class OrderAdmin(CustomImportExport):
    list_display = [field.name for field in Post._meta.fields]
    list_editable = [field.name for field in Post._meta.fields if field.name != 'id' and field.name != 'created_at']


@admin.register(MailingLog)
class MailingLogAdmin(CustomImportExport):
    list_display = [field.name for field in MailingLog._meta.fields]


@admin.register(Card)
class CardAdmin(CustomImportExport):
    list_display = [field.name for field in Card._meta.fields]
    list_editable = [field.name for field in Card._meta.fields if field.name != 'id' and field.name != 'created_at']


# sort models from admin.py by their registering (not alphabetically)
def get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request, app_label)
    app_list = list(app_dict.values())
    return app_list


admin.AdminSite.get_app_list = get_app_list
