from django.contrib import admin
from .models import Teacher, Class, Student

# 把模型註冊到後台
admin.site.register(Teacher)
admin.site.register(Class)
admin.site.register(Student)
