from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


from picturebooks.models import Picturebook
from activities.models import Task, Quiz, StudentQuizAttempt  # 👈 檢查這行有沒有 Task
from accounts.models import Student, Teacher

# ==========================================
# 🌟 全站共用：登入大廳 
# ==========================================
def public_lobby(request):
    if request.method == 'POST':
        # 1. 抓取表單傳來的帳號與密碼 (不需要 role 了！)
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        # 2. 請 Django 的保全來驗證帳密是否正確
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            # 密碼正確！正式讓他登入 (發放 session 通行證)
            login(request, user)
            
            # 3. 自動掃描他身上帶的是哪種證件！
            # hasattr 就是問：「請問這個 user 身上，有沒有掛著 teacher_profile 這個東西？」
            if hasattr(user, 'teacher_profile'):
                return redirect('teacher_dashboard') # 踢去老師大廳
                
            elif hasattr(user, 'student_profile'):
                return redirect('student_dashboard') # 踢去學生大廳
                
            else:
                # 如果是校長 (superuser) 登入，身上沒有老師或學生證
                if user.is_superuser:
                    return redirect('/admin/') # 直接請去後台
                else:
                    messages.error(request, '此帳號尚未綁定任何身分證件！')
                    return redirect('public_lobby')
        else:
            # 密碼錯誤
            messages.error(request, '帳號或密碼錯誤，請重新輸入！')
            return redirect('public_lobby')
            
    return render(request, 'public/login.html')

# ==========================================
# 第一個功能：學生大廳
# ==========================================
def student_dashboard(request):
    all_picturebooks = Picturebook.objects.all()
    all_tasks = Task.objects.all()

    dummy_user = {
        'name': '探險家小明',
        'class_name': '五年五班',
        'title': '單字新手',
        'preferences': ['科學', '旅遊']
    }
    
    dummy_leaderboard = [
        {'name': '小華', 'stars': 150},
        {'name': '小美', 'stars': 120},
        {'name': '探險家小明', 'stars': 50},
    ]

    context = {
        'books': all_picturebooks,
        'tasks': all_tasks,
        'user_profile': dummy_user,
        'leaderboard': dummy_leaderboard,
    }
    return render(request, 'student/student_dashboard.html', context)

# ==========================================
# 第二個功能：任務挑戰準備區
# ==========================================
def task_detail(request, task_id):
    task = Task.objects.get(taskid=task_id)
    context = {
        'task': task
    }
    return render(request, 'student/task_detail.html', context)

# ==========================================
# 第三個功能：真實測驗考場與自動改卷系統
# ==========================================
def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(quizid=quiz_id)

    if request.method == 'POST':
        score = 0
        total_questions = quiz.questions.count()

        for q in quiz.questions.all():
            student_answer = request.POST.get(str(q.qid))
            if student_answer == q.correct_answer:
                score += (100 / total_questions)

        current_student = Student.objects.first()
        
        StudentQuizAttempt.objects.create(
            student=current_student,
            quiz=quiz,
            score=int(score)
        )

        return redirect('student_dashboard')

    questions_data = []
    for q in quiz.questions.all():
        options_list = q.options.split(',')
        questions_data.append({
            'id': q.qid,
            'text': q.question_text,
            'options': options_list
        })

    context = {
        'quiz': quiz,
        'questions_data': questions_data
    }
    return render(request, 'student/take_quiz.html', context)

# ==========================================
# 第四個功能：教師管理大廳
# ==========================================
def teacher_dashboard(request):
    return render(request, 'teacher/teacher_dashboard.html')

# ==========================================
# 新增功能：學生端各區塊子頁面
# ==========================================
def student_level(request, grade):
    # 🌟 幫你把關卡假資料補回來了！
    dummy_levels = [
        {'id': 1, 'name': f'單元 1：打招呼'},
        {'id': 2, 'name': f'單元 2：數字與顏色'},
        {'id': 3, 'name': f'單元 3：我的家庭'},
    ]
    context = {
        'grade': grade,
        'levels': dummy_levels
    }
    return render(request, 'student/student_level.html', context)

def student_tower(request):
    dummy_tower_levels = [
        {'id': 5, 'name': '天空魔龍', 'is_unlocked': False},
        {'id': 4, 'name': '迷霧森林', 'is_unlocked': False},
        {'id': 3, 'name': '試煉遺跡', 'is_unlocked': False},
        {'id': 2, 'name': '哥布林洞穴', 'is_unlocked': False},
        {'id': 1, 'name': '史萊姆平原', 'is_unlocked': True}, 
    ]
    context = {
        'tower_levels': dummy_tower_levels
    }
    return render(request, 'student/student_tower.html', context)

def student_store(request):
    dummy_stars = 50
    dummy_items = [
        {'name': '學習文具組', 'cost': 100},
        {'name': '神秘小禮物', 'cost': 300},
        {'name': '免寫作業卡', 'cost': 1000},
        {'name': '自訂酷炫稱號', 'cost': 500},
    ]
    context = {
        'stars': dummy_stars,
        'items': dummy_items
    }
    return render(request, 'student/student_store.html', context)