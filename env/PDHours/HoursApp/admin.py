from django.contrib import admin
from .models import Squad,User,Report

class UserAdmin(admin.ModelAdmin):
    
    list_display = ('name','get_assigned_squad','user_estimated_hours')
    readonly_fields = ['user_estimated_hours']
    
admin.site.register(User, UserAdmin)

class SquadAdmin(admin.ModelAdmin): 
    list_display = ('name','get_squad_users')
admin.site.register(Squad, SquadAdmin)

class ReportAdmin(admin.ModelAdmin): 
    list_display = ('id','get_author','spent_hours','created_at')
  
admin.site.register(Report, ReportAdmin)

