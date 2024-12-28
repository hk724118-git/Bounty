from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from datetime import datetime

class CustomUserManager(BaseUserManager):
    def create_user(self, telephone, password=None, is_admin=False, is_publisher=False, **extra_fields):
        if not telephone:
            raise ValueError('电话号必填')
        user = self.model(telephone=telephone, is_admin=is_admin, is_publisher=is_publisher, **extra_fields)
        user.set_password(password)
        user.last_login = None
        user.save(using=self._db)
        return user

    def create_superuser(self, telephone, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('last_login', datetime.now())

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        return self.create_user(telephone, password, **extra_fields)

class Admin(AbstractBaseUser):
    AccountID = models.AutoField(primary_key=True, verbose_name="账号ID")
    telephone = models.CharField(max_length=15, verbose_name="电话", unique=True)
    is_admin = models.BooleanField(default=False, verbose_name="是否管理员")  # 默认值为 False
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="最后登录时间")

    objects = CustomUserManager()

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'admin'  # 明确指定表名

    def __str__(self):
        return self.telephone

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

class Publisher(AbstractBaseUser):
    AccountID = models.AutoField(primary_key=True, verbose_name="账号ID")
    telephone = models.CharField(max_length=15, verbose_name="电话", unique=True)  # 确保字段名一致
    is_publisher = models.BooleanField(default=False, verbose_name="是否发布者")  # 发布者默认不是发布者
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="最后登录时间")

    objects = CustomUserManager()

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'publishers'  # 明确指定表名

    def __str__(self):
        return self.telephone

    def has_perm(self, perm, obj=None):
        return False

    def has_module_perms(self, app_label):
        return False

    @property
    def is_staff(self):
        return self.is_publisher

class Receiver(AbstractBaseUser):
    AccountID = models.AutoField(primary_key=True, verbose_name="账号ID")
    telephone = models.CharField(max_length=15, verbose_name="电话", unique=True)  # 确保字段名一致
    is_receiver = models.BooleanField(default=False, verbose_name="是否接收者")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="最后登录时间")

    objects = CustomUserManager()

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'receivers'  # 明确指定表名

    def __str__(self):
        return self.telephone

    def has_perm(self, perm, obj=None):
        return False

    def has_module_perms(self, app_label):
        return False

    @property
    def is_staff(self):
        return self.is_receiver

from django.utils import timezone

class Task(models.Model):
    TASK_TYPES = [
        ('购物', '购物'),
        ('送物', '送物'),
        ('打扫', '打扫'),
        ('取件', '取件'),
        ('其他', '其他'),
    ]

    TaskID = models.AutoField(primary_key=True)
    PublishTime = models.DateTimeField(auto_now_add=True)
    Payment = models.DecimalField(max_digits=10, decimal_places=2)
    Content = models.TextField()
    Deadline = models.DateTimeField()
    TaskType = models.CharField(max_length=50, choices=TASK_TYPES)
    Alocation = models.CharField(max_length=100)

    def __str__(self):
        return self.Content

    class Meta:
        db_table = 'tasks'  # 指定模型映射的数据库表名

class Evidence(models.Model):
    EvidenceID = models.AutoField(primary_key=True)
    Text = models.TextField()
    Image = models.ImageField(upload_to='evidence_images/', blank=True, null=True)
    Video = models.FileField(upload_to='evidence_videos/', blank=True, null=True)

    def __str__(self):
        return f"Evidence {self.EvidenceID}"

    class Meta:
        db_table = 'evidence'