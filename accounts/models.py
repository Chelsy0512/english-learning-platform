from django.db import models
from django.contrib.auth.models import User  # 🌟 匯入 Django 最強大的內建 User 系統

# 教師模型
class Teacher(models.Model):
    tid = models.AutoField(primary_key=True)
    # 🌟 發放識別證：將這個老師綁定到一個 Django User 帳號上
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='teacher_profile')
    
    name = models.CharField(max_length=100, verbose_name="姓名")
    total_points = models.IntegerField(default=0, verbose_name="總積分")
    # 💡 移除了 email 和 passwd，因為 User 模型已經自帶了！

    def __str__(self):
        return self.name

# 班級模型 (維持不變)
class Class(models.Model):
    cid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="班級名稱")
    tid = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classes')

    def __str__(self):
        return self.name

# 學生模型
class Student(models.Model):
    sid = models.AutoField(primary_key=True)
    # 🌟 發放識別證：將這個學生綁定到一個 Django User 帳號上
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='student_profile')
    
    name = models.CharField(max_length=100, verbose_name="姓名")
    nickname = models.CharField(max_length=100, blank=True, null=True, verbose_name="暱稱")
    total_points = models.IntegerField(default=0, verbose_name="總積分")
    # 💡 移除了 email 和 passwd！
    
    cid = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='students')

    def __str__(self):
        return f"{self.name} ({self.nickname})"