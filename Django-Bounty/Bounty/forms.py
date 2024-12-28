from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Admin, Publisher, Receiver, Task, Evidence

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Admin
        fields = ('telephone',)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['telephone'].widget.attrs.update({'class': 'input-field', 'placeholder': '电话', 'required': 'required'})
        self.fields['password1'].widget.attrs.update({'class': 'input-field', 'placeholder': '密码', 'required': 'required'})
        self.fields['password2'].widget.attrs.update({'class': 'input-field', 'placeholder': '确认密码', 'required': 'required'})

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '电话'
        self.fields['username'].widget.attrs.update({'class': 'input-field', 'placeholder': '电话', 'required': 'required'})
        self.fields['password'].widget.attrs.update({'class': 'input-field', 'placeholder': '密码', 'required': 'required'})

    def confirm_login_allowed(self, user):
        if not user.is_active or not user.is_admin:
            raise forms.ValidationError('该账号不存在')

class PublisherCreationForm(UserCreationForm):
    class Meta:
        model = Publisher
        fields = ('telephone',)

    def __init__(self, *args, **kwargs):
        super(PublisherCreationForm, self).__init__(*args, **kwargs)
        self.fields['telephone'].widget.attrs.update({'class': 'input-field', 'placeholder': '电话', 'required': 'required'})
        self.fields['password1'].widget.attrs.update({'class': 'input-field', 'placeholder': '密码', 'required': 'required'})
        self.fields['password2'].widget.attrs.update({'class': 'input-field', 'placeholder': '确认密码', 'required': 'required'})

    def save(self, commit=True):
        user = super(PublisherCreationForm, self).save(commit=False)
        user.is_publisher = True
        user.is_active = True
        if commit:
            user.save()
        return user


class PublisherAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(PublisherAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '电话'
        self.fields['username'].widget.attrs.update({'class': 'input-field', 'placeholder': '电话', 'required': 'required'})
        self.fields['password'].widget.attrs.update({'class': 'input-field', 'placeholder': '密码', 'required': 'required'})

    def confirm_login_allowed(self, user):
        if not user.is_active or not getattr(user, 'is_publisher', False):
            raise forms.ValidationError('您不是发布者。')

class ReceiverCreationForm(UserCreationForm):
    class Meta:
        model = Receiver
        fields = ('telephone',)

    def __init__(self, *args, **kwargs):
        super(ReceiverCreationForm, self).__init__(*args, **kwargs)
        self.fields['telephone'].widget.attrs.update({'class': 'input-field', 'placeholder': '电话', 'required': 'required'})
        self.fields['password1'].widget.attrs.update({'class': 'input-field', 'placeholder': '密码', 'required': 'required'})
        self.fields['password2'].widget.attrs.update({'class': 'input-field', 'placeholder': '确认密码', 'required': 'required'})

    def save(self, commit=True):
        user = super(ReceiverCreationForm, self).save(commit=False)
        user.is_receiver = True
        user.is_active = True
        if commit:
            user.save()
        return user


class ReceiverAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(ReceiverAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '电话'
        self.fields['username'].widget.attrs.update({'class': 'input-field', 'placeholder': '电话', 'required': 'required'})
        self.fields['password'].widget.attrs.update({'class': 'input-field', 'placeholder': '密码', 'required': 'required'})

    def confirm_login_allowed(self, user):
        if not user.is_active or not getattr(user, 'is_receiver', False):
            raise forms.ValidationError('您不是接收者。')


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('TaskType', 'Content', 'Alocation', 'Deadline', 'Payment')
        widgets = {
            'TaskType': forms.Select(attrs={'class': 'input-field', 'required': 'required'}),
            'Content': forms.Textarea(attrs={'class': 'input-field', 'rows': 5, 'placeholder': '任务描述', 'required': 'required'}),
            'Alocation': forms.TextInput(attrs={'class': 'input-field', 'placeholder': '任务地点', 'required': 'required'}),
            'Deadline': forms.DateTimeInput(attrs={'class': 'input-field', 'type': 'datetime-local', 'required': 'required'}),
            'Payment': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': '酬金', 'required': 'required'}),  # 修改为 NumberInput
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['TaskType'].choices = Task.TASK_TYPES

class EvidenceForm(forms.ModelForm):
    class Meta:
        model = Evidence
        fields = ('Text', 'Image', 'Video')
        widgets = {
            'Text': forms.Textarea(attrs={'class': 'input-field', 'rows': 5, 'placeholder': '证据文本', 'required': 'required'}),
            'Image': forms.ClearableFileInput(attrs={'class': 'input-field'}),
            'Video': forms.ClearableFileInput(attrs={'class': 'input-field'}),
        }

    def __init__(self, *args, **kwargs):
        super(EvidenceForm, self).__init__(*args, **kwargs)
        self.fields['Text'].required = True
        self.fields['Image'].required = False  # 图片字段可选
        self.fields['Video'].required = False  # 视频字段可选