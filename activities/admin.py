from django.contrib import admin
#  1. 匯入的後台模組
from import_export.admin import ImportExportModelAdmin 
from .models import Achievement, StudentAchievement, Activity, Question, Quiz, StudentQuizAttempt, Task

#  2. 幫 Question 寫一個專屬的後台設定，讓它繼承題目表！
class QuestionAdmin(ImportExportModelAdmin):
    # 這裡可以順便設定後台列表要顯示哪些欄位，讓畫面更好看
    list_display = ('qid', 'question_text', 'correct_answer')

# ================= 把模型註冊到後台 =================
#  3. 注意這裡！把 Question 跟剛剛寫好的 QuestionAdmin 綁在一起註冊
admin.site.register(Question, QuestionAdmin)

# 以下其他模型照舊，維持原樣
admin.site.register(Achievement)
admin.site.register(StudentAchievement)
admin.site.register(Quiz)
admin.site.register(StudentQuizAttempt)
admin.site.register(Activity)
admin.site.register(Task)