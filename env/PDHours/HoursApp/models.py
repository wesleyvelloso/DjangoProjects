from django.db import models
from django.db.models import Sum
from datetime import timedelta

class Squad(models.Model):
    name = models.CharField('Squad Name',max_length=100) 
    
    def get_squad_users(self):
        cur_users = self.user_squad.all()
        users = [u.name for u in cur_users]
        return users

    get_squad_users.short_description = "Squad members"
    
    class Meta:
        db_table = 'Squad'
    def __str__(self):
       return self.name
            
class User(models.Model):
    id = models.CharField(max_length=11,verbose_name='Personal ID', primary_key=True)
    name = models.CharField(max_length=100,verbose_name='Name') 
    user_estimated_hours = models.DurationField(db_column='user_estimated_hours',help_text = 'Time in format: (HH:MM:SS)',blank=True,null=True,)
    
    squadid = models.ForeignKey(Squad, db_column='squadid',default=1, verbose_name='Squad',related_name="user_squad",on_delete=models.CASCADE)
    
    def get_assigned_squad(self): 
        return self.squadid.name
    
    get_assigned_squad.short_description = "Assigned squad"
    
    def timedelta(self):
        try:
            return timedelta(seconds=self.sum)
        except AttributeError:
            return None
    
    class Meta: 
        db_table = 'User'
    def __str__(self):
           return self.name
        
class Report(models.Model):
    id = models.CharField(max_length=30,verbose_name='Title', primary_key=True)
    description = models.TextField()
    spent_hours = models.DurationField(db_column='spent_hours',help_text = 'Time in format: (HH:MM:SS)',blank=True,null=True)
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    userId = models.ForeignKey(User,db_column='userId',related_name="user_reports",on_delete=models.CASCADE) 
      
    def save(self, *args, **kwargs):   
        super(Report, self).save(*args, **kwargs)
        user_obj = self.userId
        user_obj.user_estimated_hours = (user_obj.user_estimated_hours) - (user_obj.self.spent_hours)
        user_obj.save() 
        
    def timedelta(self):
        try:
            return timedelta(seconds=self.sum)
        except AttributeError:
            return None
        
    def get_author(self): 
        return self.userId.name
    
    get_author.short_description = "Author"
    
    class Meta: 
        db_table = 'Report'
        
    def __str__(self):
           return self.userId.name