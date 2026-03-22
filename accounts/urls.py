from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    # <int:task_id> 代表網址這裡會接收一個數字 (任務ID)
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
]