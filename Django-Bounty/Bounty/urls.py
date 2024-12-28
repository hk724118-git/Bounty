from django.urls import path
from . import views

app_name = 'Bounty'

urlpatterns = [
    path('', views.index, name='index'),
    path('index1/', views.index_publisher, name='index1'),
    path('index2/', views.index_receiver, name='index2'),
    path('adminSignup/', views.adminSignup, name='adminSignup'),  # 管理员注册
    path('publisherSignup/', views.publisherSignup, name='publisherSignup'),  # 发布者注册
    path('recieverSignup/', views.recieverSignup, name='recieverSignup'),  # 接收者注册
    path('my_orders/', views.my_orders, name='my_orders'),
    path('publish-task/', views.publish_task, name='publish_task'),
    path('upload_evidence/', views.upload_evidence, name='upload_evidence'),
    path('task-list/', views.task_list, name='task_list'),
    path('getTask/<int:task_id>/', views.get_task, name='get_task'),
    path('task-list1/', views.task_list1, name='task_list1'),
    path('getTask1/<int:task_id>/', views.get_task1, name='get_task1'),
    path('task-list2/', views.task_list2, name='task_list2'),
    path('getTask2/<int:task_id>/', views.get_task2, name='get_task2'),
    path('my_tasks/', views.my_tasks, name='my_tasks'),
    path('my_messages/', views.my_messages, name='my_messages'),
    path('selectID/', views.selectID, name='selectID'),
    path('logout/', views.logout_view, name='logout'),
    path('selectIDlg/', views.selectIDlg, name='selectIDlg'),
    path('publisherLogin/', views.publisherLogin, name='publisherLogin'),  # 发布者登录
    path('recieverLogin/', views.recieverLogin, name='recieverLogin'),  # 接收者登录
    path('adminLogin/', views.adminLogin, name='adminLogin'),  # 管理员登录
    path('adminInfo/', views.adminInfo, name='adminInfo'),
    path('publisherIfm/', views.publisherIfm, name='publisherIfm'),
    path('recieverInfo/', views.recieverInfo, name='recieverInfo'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
]