from django.db import models
# 這裡多匯入了 Teacher 和 Class，因為測驗和任務會用到他們
from accounts.models import Student, Teacher, Class 

# ================= 1. 成就系統 (之前寫好的) =================
class Achievement(models.Model):
    achievementid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="成就名稱")
    description = models.TextField(verbose_name="成就描述")
    icon_url = models.URLField(blank=True, null=True, verbose_name="成就圖示連結")

    def __str__(self):
        return self.name

class StudentAchievement(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='unlocked_by')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='achievements')
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'achievement')

    def __str__(self):
        return f"{self.student.name} 解鎖了 [{self.achievement.name}]"


# ================= 2. 測驗與題目系統 =================
class Question(models.Model):
    qid = models.AutoField(primary_key=True)
    question_text = models.TextField(verbose_name="題目內容")
    correct_answer = models.CharField(max_length=200, verbose_name="正確答案")
    options = models.TextField(verbose_name="選項(可用逗號分隔)")
    tid = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="出題老師")

    def __str__(self):
        return self.question_text[:20]

class Quiz(models.Model):
    quizid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="測驗標題")
    target_vocabulary = models.TextField(verbose_name="目標單字")
    tid = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="出題老師")
    
    # 這行會自動建立 ERD 上的「Quiz_Question_Rel」表格
    questions = models.ManyToManyField(Question, related_name='quizzes', verbose_name="包含題目")

    def __str__(self):
        return self.title

# 學生測驗成績紀錄
class StudentQuizAttempt(models.Model):
    attemptid = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="作答學生")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name="測驗卷")
    score = models.IntegerField(verbose_name="分數")
    attempted_at = models.DateTimeField(auto_now_add=True, verbose_name="作答時間")

    def __str__(self):
        return f"{self.student.name} - {self.quiz.title} ({self.score}分)"


# ================= 3. 任務與活動系統 =================
# 因為 ERD 中 Task 需要連到 Activity，所以 Activity 要建出來
class Activity(models.Model):
    aid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name="活動名稱")
    content = models.TextField(verbose_name="活動內容")
    type = models.CharField(max_length=50, verbose_name="活動類型")
    reward = models.IntegerField(verbose_name="獎勵積分")
    
    def __str__(self):
        return self.name

class Task(models.Model):
    taskid = models.AutoField(primary_key=True)
    # 任務是由哪位老師(tid)、指派給哪個班級(cid)、做哪項活動(aid)
    tid = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="指派老師")
    cid = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="指派班級")
    aid = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name="指定活動")
    
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name="指派時間")
    due_date = models.DateTimeField(verbose_name="截止日期")

    def __str__(self):
        return f"{self.cid.name} 的任務: {self.aid.name}"