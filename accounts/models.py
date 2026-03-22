from django.db import models

# 教師模型
class Teacher(models.Model):
    tid = models.AutoField(primary_key=True) # 自動遞增編號
    name = models.CharField(max_length=100, verbose_name="姓名")
    email = models.EmailField(unique=True, verbose_name="電子郵件")
    passwd = models.CharField(max_length=128, verbose_name="密碼")
    total_points = models.IntegerField(default=0, verbose_name="總積分")

    def __str__(self):
        return self.name

# 班級模型
class Class(models.Model):
    cid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="班級名稱")
    # ForeignKey 對應 ERD，表示多個班級可以屬於一位老師
    tid = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classes')

    def __str__(self):
        return self.name

# 學生模型
class Student(models.Model):
    sid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="姓名")
    nickname = models.CharField(max_length=100, blank=True, null=True, verbose_name="暱稱")
    email = models.EmailField(unique=True, verbose_name="電子郵件")
    passwd = models.CharField(max_length=128, verbose_name="密碼")
    total_points = models.IntegerField(default=0, verbose_name="總積分")
    # ForeignKey 對應 ERD，表示多個學生屬於一個班級
    cid = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='students')

    def __str__(self):
        return f"{self.name} ({self.nickname})"