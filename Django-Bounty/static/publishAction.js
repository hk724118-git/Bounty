const form = document.getElementById('publish-task');
const type = document.getElementById('id_TaskType');
const description = document.getElementById('id_Content');
const alocation = document.getElementById('id_Alocation');
const dueDate = document.getElementById('id_Deadline');
const reward = document.getElementById('id_Payment');

// 为表单绑定 submit 事件处理程序
form.addEventListener('submit', async function (event) {
    event.preventDefault();

    // 表单校验
    const requiredFields = [type, description, alocation, dueDate, reward];
    if (requiredFields.some(field => !field.value)) {
        alert('所有字段都是必填的');
        return;
    }

    // 创建一个新的任务对象
    const task = {
        TaskType: type.value,
        Content: description.value,
        Alocation: alocation.value,
        Deadline: dueDate.value,
        Payment: parseFloat(reward.value)  // 确保 Payment 是有效的数字
    };

    try {
        // 获取 CSRF 令牌
        const csrftoken = getCookie('csrftoken');

        // 发送 POST 请求将任务列表加入到后端任务列表
        const response = await fetch('/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(task)
        });

        // 如果请求成功，跳转到任务列表页面
        if (response.ok) {
            alert('任务发布成功！');
            window.location.href = '../index.html';
        } else {
            const data = await response.json();
            alert(data.error || '任务发布失败');
            console.error('Response:', data);
        }
    } catch (error) {
        // 如果请求失败，提示用户并将错误信息记录在控制台
        alert('任务发布失败');
        console.error('Error:', error);
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}