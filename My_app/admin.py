from django.contrib import admin

from .models import Project, Service, Inquiry, Document
# Register your models here.
admin.site.register(Project)
admin.site.register(Service)
admin.site.register(Inquiry)
admin.site.register(Document)
