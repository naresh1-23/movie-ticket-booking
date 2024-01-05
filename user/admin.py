from django.contrib.admin import register, ModelAdmin
from .models import User

@register(User)
class UserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'mobile_number')



# Register your models here.
