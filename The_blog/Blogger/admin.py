from django.contrib import admin
from .models import Post, BlogComment
# Register your models here.

admin.site.register((BlogComment))

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ("tinyinject.js",)
        
        ''' In the above line we just add our javascript file to admin page but as u can see 
        there is a tuple which containing only one file so it's very important to note that
        when u have only one file in tuple at that time u have to put comma(,) after file it is necessary '''
