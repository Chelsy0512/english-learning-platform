from django.db import models
from accounts.models import Student  # 🌟 重要：我們要從帳號 App 借用剛寫好的「學生」模型！

# 繪本模型
class Picturebook(models.Model):
    pid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="繪本標題")
    style = models.CharField(max_length=100, verbose_name="繪圖風格")
    target_vocabulary = models.TextField(verbose_name="目標單字") # 可以儲存 AI 產生的目標單字
    grade = models.CharField(max_length=50, verbose_name="適用年級")
    lesson = models.CharField(max_length=100, verbose_name="單元名稱")
    
    # ForeignKey 對應 ERD 中的 sid，代表這本繪本是專屬於哪位學生的
    sid = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='picturebooks', verbose_name="所屬學生")
    
    # 我幫你加了一個建立時間，這樣以後學生的學習歷程才能照時間排序！
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    def __str__(self):
        return f"{self.title} - {self.sid.name}"
