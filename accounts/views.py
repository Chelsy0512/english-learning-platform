from django.shortcuts import render
# 匯入繪本和任務模型
from picturebooks.models import Picturebook
from activities.models import Task

# 第一個功能：學生大廳
def student_dashboard(request):
    all_picturebooks = Picturebook.objects.all()
    all_tasks = Task.objects.all()

    context = {
        'books': all_picturebooks,
        'tasks': all_tasks,
    }
    return render(request, 'accounts/student_dashboard.html', context)

# ==========================================
# 🌟 第二個功能：任務挑戰畫面 (剛剛找不到的就是它！)
# ==========================================
def task_detail(request, task_id):
    # 用 task_id 去資料庫找出是哪一個任務
    task = Task.objects.get(taskid=task_id)
    
    # 把這個任務打包，準備送給 HTML 顯示
    context = {
        'task': task
    }
    return render(request, 'accounts/task_detail.html', context)