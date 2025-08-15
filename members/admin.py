from django.contrib import admin
from .models import Profile,FollowRequest,Follow

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(FollowRequest)
class FollowRequestAdmin(admin.ModelAdmin):
    pass

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass

