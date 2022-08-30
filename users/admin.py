from django.contrib import admin
from users.models import *

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ('followed', 'follower')})]
    list_display = ('followed', 'follower')