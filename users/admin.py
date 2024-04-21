from django.contrib import admin
from .models import User, EmailVerification
from products.admin import BasketAdmin

class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (BasketAdmin, )

admin.site.register(User, UserAdmin)

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'created')
    readonly_fields = ('created', )