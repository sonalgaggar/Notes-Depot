from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    name=models.CharField(unique=True, max_length=150,db_index=True)
    slug=models.SlugField(unique=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('story_category',args=[self.slug])


class Notes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    uploadingdate=models.CharField(max_length=30)
    
    subject=models.ForeignKey(Category,on_delete=models.CASCADE)
    notesfile=models.FileField(null=True)
    filetype=models.CharField(max_length=30)
    descriptions=models.CharField(max_length=200,null=True)
    status=models.CharField(max_length=15)
    


    def __str__(self):
        return self.user.username+" "+self.status