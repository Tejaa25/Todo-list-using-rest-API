from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save #post_save is also there.
#pre save is bcz we have to save the slug before saving task instance
from todoREST.utils import unique_slug_generator
# Create your models here.
class Task(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    #CASCADE: When the referenced object is deleted, also delete the objects that have references to it
    #models.restrict is dont allow to delete
    slug=models.SlugField(max_length=250,null=True,blank=True)
    #we use slug to save the title(eg. My Title) in the task as slugfield(eg. my-title)
    #whenever we hit http://127.0.0.1:8000/home/1 it will retrieve the task id 1
    #instead of enter id , we can enter title http://127.0.0.1:8000/home/My Title
    #for space it will automatically takes as http://127.0.0.1:8000/home/My%20Title
    #so to prevent that we changing our title to slug field http://127.0.0.1:8000/home/my-title
    title=models.CharField(max_length=50)
    desc=models.TextField(null=True,blank=True)
    completed=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title

def slug_generator(sender,instance,*args, **kwargs):
    if not instance.slug:
        instance.slug=unique_slug_generator(instance)

pre_save.connect(slug_generator,sender=Task)
