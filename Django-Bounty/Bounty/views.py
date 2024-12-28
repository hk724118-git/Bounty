from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, PublisherCreationForm, PublisherAuthenticationForm, ReceiverCreationForm, ReceiverAuthenticationForm
from .models import Admin, Publisher, Receiver
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from .forms import TaskForm, EvidenceForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task
import json
import logging

def index(request):
    return render(request, 'index.html')

def index_publisher(request):
    return render(request, 'index1.html')

def index_receiver(request):
    return render(request, 'index2.html')

def adminSignup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_admin = True
            user.save()
            login(request, user)
            return redirect('Bounty:index')
        else:
            form.add_error(None, '表单验证错误')
    else:
        form = CustomUserCreationForm()
    return render(request, 'adminSignup.html', {'form': form})

def publisherSignup(request):
    if request.method == 'POST':
        form = PublisherCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('Bounty:index')  # 注册成功后跳转到登录页面
    else:
        form = PublisherCreationForm()
    return render(request, 'publisherSignup.html', {'form': form})

def recieverSignup(request):
    if request.method == 'POST':
        form = ReceiverCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('Bounty:index')  # 注册成功后跳转到登录页面

    else:
        form = ReceiverCreationForm()
    return render(request, 'recieverSignup.html', {'form': form})

def publisherLogin(request):
    if request.method == 'POST':
        telephone = request.POST.get('username')
        password = request.POST.get('password')

        pub = Publisher.objects.filter(telephone=telephone, is_publisher=True).last()
        if pub:
            if check_password(password, pub.password):
                login(request, pub)
                next_url = request.POST.get('next', 'Bounty:index1')
                return redirect(next_url)
            else:
                form = PublisherAuthenticationForm(request, data=request.POST)
                form.add_error(None, '密码错误。')
        else:
            form = PublisherAuthenticationForm(request, data=request.POST)
            form.add_error(None, '该电话号码未注册为发布者。')
    else:
        form = PublisherAuthenticationForm()

    return render(request, 'publisherLogin.html', {'form': form})

def recieverLogin(request):
    if request.method == 'POST':
        telephone = request.POST.get('username')
        password = request.POST.get('password')

        pub = Receiver.objects.filter(telephone=telephone, is_receiver=True).last()
        if pub:
            if check_password(password, pub.password):
                login(request, pub)
                next_url = request.POST.get('next', 'Bounty:index2')
                return redirect(next_url)
            else:
                form = ReceiverAuthenticationForm(request, data=request.POST)
                form.add_error(None, '密码错误。')
        else:
            form = ReceiverAuthenticationForm(request, data=request.POST)
            form.add_error(None, '该电话号码未注册为接收者。')
    else:
        form = ReceiverAuthenticationForm()

    return render(request, 'recieverLogin.html', {'form': form})

def adminLogin(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_admin:
                login(request, user)
                return redirect('Bounty:adminInfo')
            else:
                form.add_error(None, '您不是管理员。')
        else:
            form.add_error(None, '用户名或密码错误。')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'adminLogin.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('Bounty:selectIDlg')

logger = logging.getLogger(__name__)

def publish_task(request):
    logger.info('publish_task view called')
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = TaskForm()
    return render(request, 'publish-task.html', {'form': form})

logger = logging.getLogger(__name__)

def task_list(request):
    tasks = Task.objects.all()
    task_data = [
        {
            'id': task.TaskID,
            'name': f'任务{task.TaskID}',
            'type': task.TaskType,
            'dueDate': task.Deadline.strftime('%Y-%m-%d %H:%M:%S'),
            'alocation': task.Alocation,
            'reward': float(task.Payment)
        }
        for task in tasks
    ]
    logger.debug(f"Task list: {task_data}")
    return render(request, 'task-list.html', {'tasks_json': json.dumps(task_data)})

def get_task(request, task_id):
    logger.debug(f"Trying to get task with TaskID: {task_id}")
    task = get_object_or_404(Task, TaskID=task_id)
    task_data = {
        'type': task.TaskType,
        'description': task.Content,
        'alocation': task.Alocation,
        'dueDate': task.Deadline.strftime('%Y-%m-%d %H:%M:%S'),
        'reward': float(task.Payment)
    }
    logger.debug(f"Task found: {task_data}")
    return render(request, 'getTask.html', {'task': task_data})

def task_list1(request):
    tasks = Task.objects.all()
    task_data = [
        {
            'id': task.TaskID,
            'name': f'任务{task.TaskID}',
            'type': task.TaskType,
            'dueDate': task.Deadline.strftime('%Y-%m-%d %H:%M:%S'),
            'alocation': task.Alocation,
            'reward': float(task.Payment)
        }
        for task in tasks
    ]
    logger.debug(f"Task list: {task_data}")
    return render(request, 'task-list1.html', {'tasks_json': json.dumps(task_data)})

def get_task1(request, task_id):
    logger.debug(f"Trying to get task with TaskID: {task_id}")
    task = get_object_or_404(Task, TaskID=task_id)
    task_data = {
        'type': task.TaskType,
        'description': task.Content,
        'alocation': task.Alocation,
        'dueDate': task.Deadline.strftime('%Y-%m-%d %H:%M:%S'),
        'reward': float(task.Payment)
    }
    logger.debug(f"Task found: {task_data}")
    return render(request, 'getTask1.html', {'task': task_data})

def task_list2(request):
    tasks = Task.objects.all()
    task_data = [
        {
            'id': task.TaskID,
            'name': f'任务{task.TaskID}',
            'type': task.TaskType,
            'dueDate': task.Deadline.strftime('%Y-%m-%d %H:%M:%S'),
            'alocation': task.Alocation,
            'reward': float(task.Payment)
        }
        for task in tasks
    ]
    logger.debug(f"Task list: {task_data}")
    return render(request, 'task-list2.html', {'tasks_json': json.dumps(task_data)})

def get_task2(request, task_id):
    logger.debug(f"Trying to get task with TaskID: {task_id}")
    task = get_object_or_404(Task, TaskID=task_id)
    task_data = {
        'type': task.TaskType,
        'description': task.Content,
        'alocation': task.Alocation,
        'dueDate': task.Deadline.strftime('%Y-%m-%d %H:%M:%S'),
        'reward': float(task.Payment)
    }
    logger.debug(f"Task found: {task_data}")
    return render(request, 'getTask2.html', {'task': task_data})

def upload_evidence(request):
    logger.info('upload_evidence view called')
    if request.method == 'POST':
        form = EvidenceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = EvidenceForm()
    return render(request, 'upload_evidence.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_publisher, login_url='Bounty:selectIDlg')
def my_orders(request):
    orders = []
    return render(request, 'my_orders.html', {'orders': orders})

@login_required
@user_passes_test(lambda u: u.is_reciever, login_url='Bounty:selectIDlg')
def my_tasks(request):
    tasks = []
    return render(request, 'my_tasks.html', {'tasks': tasks})

@login_required
@user_passes_test(lambda u: u.is_admin, login_url='Bounty:selectIDlg')
def my_messages(request):
    messages = []
    return render(request, 'my_messages.html', {'messages': messages})


@login_required
@user_passes_test(lambda u: u.is_reciever, login_url='Bounty:selectIDlg')
def recieverDashboard(request):
    return render(request, 'recieverDashboard.html')

def selectID(request):
    return render(request, 'selectID.html')

def selectIDlg(request):
    return render(request, 'selectIDlg.html')

def forgotPassword(request):
    # 假设这是忘记密码视图函数
    return render(request, 'forgot.html')

@login_required
def adminInfo(request):
    admin = request.user
    return render(request, 'adminInfo.html', {'admin': admin})


def publisherIfm(request):
    publisher = request.user
    return render(request, 'publisherIfm.html', {'publisher': publisher})

def recieverInfo(request):
    reciever = request.user
    return render(request, 'recieverInfo.html', {'reciever': reciever})