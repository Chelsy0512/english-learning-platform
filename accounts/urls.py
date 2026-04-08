from django.urls import path
from . import views

urlpatterns = [
    # 🌟 網站的真正首頁：登入大廳 (空字串 '' 代表 127.0.0.1:8000/)
    path('', views.public_lobby, name='public_lobby'),

    # --- 學生端 ---
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('student/quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    
    # 學生端：新擴充的探索頁面
    path('student/level/<int:grade>/', views.student_level, name='student_level'),
    path('student/tower/', views.student_tower, name='student_tower'),
    path('student/store/', views.student_store, name='student_store'),
    
    # --- 老師端 ---
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
]