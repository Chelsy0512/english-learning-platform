from django.contrib import admin
from django.urls import path, include # 🌟 記得這裡要多匯入一個 include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 只要網址開頭是 student/ 的，全部轉交給 accounts.urls 處理
    path('student/', include('accounts.urls')), 
]