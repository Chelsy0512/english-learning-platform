from django.contrib import admin
from .models import Picturebook

# 把模型註冊到後台
admin.site.register(Picturebook)