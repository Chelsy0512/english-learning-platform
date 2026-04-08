from django.contrib import admin
from .models import Teacher, Class, Student

# 告訴 Django 後台：我要管理這三個資料表！
admin.site.register(Teacher)
admin.site.register(Class)
admin.site.register(Student)