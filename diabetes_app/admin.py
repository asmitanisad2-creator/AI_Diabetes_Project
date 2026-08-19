from django.contrib import admin
from .models import Patient, Contact

admin.site.register(Patient)
admin.site.register(Contact)

from django.contrib import admin

from .models import Patient, ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "subject",
        "created_at"
    )

    search_fields = (
        "name",
        "email",
        "subject"
    )

    list_filter = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )