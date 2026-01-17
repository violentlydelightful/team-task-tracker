// Task Modal
function openTaskModal(taskId = null) {
    const modal = document.getElementById('task-modal');
    const form = document.getElementById('task-form');
    const title = document.getElementById('modal-title');
    const deleteBtn = document.getElementById('delete-task-btn');

    form.reset();
    document.getElementById('task-id').value = '';

    if (taskId) {
        title.textContent = 'Edit Task';
        deleteBtn.style.display = 'block';
        document.getElementById('task-id').value = taskId;
        // In a real app, you'd fetch task data here
        // For now, we'll just open the modal
    } else {
        title.textContent = 'New Task';
        deleteBtn.style.display = 'none';
    }

    modal.classList.add('active');
}

function closeTaskModal() {
    document.getElementById('task-modal').classList.remove('active');
}

async function saveTask(event) {
    event.preventDefault();

    const taskId = document.getElementById('task-id').value;
    const data = {
        title: document.getElementById('task-title-input').value,
        status: document.getElementById('task-status-input').value,
        priority: document.getElementById('task-priority-input').value,
        project: document.getElementById('task-project-input').value,
        due_date: document.getElementById('task-due-input').value,
        assignee_id: document.getElementById('task-assignee-input').value || null,
        description: document.getElementById('task-description-input').value
    };

    try {
        const url = taskId ? `/api/task/${taskId}` : '/api/task';
        const method = taskId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            window.location.reload();
        } else {
            alert('Failed to save task');
        }
    } catch (error) {
        alert('Error saving task: ' + error.message);
    }
}

async function deleteTask() {
    const taskId = document.getElementById('task-id').value;
    if (!taskId) return;

    if (!confirm('Are you sure you want to delete this task?')) return;

    try {
        const response = await fetch(`/api/task/${taskId}`, { method: 'DELETE' });
        if (response.ok) {
            window.location.reload();
        } else {
            alert('Failed to delete task');
        }
    } catch (error) {
        alert('Error deleting task: ' + error.message);
    }
}

// Member Modal
function openMemberModal() {
    document.getElementById('member-modal').classList.add('active');
}

function closeMemberModal() {
    document.getElementById('member-modal').classList.remove('active');
}

async function saveMember(event) {
    event.preventDefault();

    const data = {
        name: document.getElementById('member-name').value,
        email: document.getElementById('member-email').value,
        role: document.getElementById('member-role').value,
        avatar_color: document.querySelector('input[name="avatar-color"]:checked').value
    };

    try {
        const response = await fetch('/api/member', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            window.location.reload();
        } else {
            alert('Failed to add member');
        }
    } catch (error) {
        alert('Error adding member: ' + error.message);
    }
}

// Drag and Drop for Board
function dragTask(event) {
    event.dataTransfer.setData('taskId', event.target.dataset.taskId);
}

function allowDrop(event) {
    event.preventDefault();
}

async function dropTask(event) {
    event.preventDefault();
    const taskId = event.dataTransfer.getData('taskId');
    const column = event.target.closest('.board-column');

    if (!column || !taskId) return;

    const newStatus = column.dataset.status;

    try {
        const response = await fetch(`/api/task/${taskId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });

        if (response.ok) {
            window.location.reload();
        }
    } catch (error) {
        console.error('Error updating task:', error);
    }
}

// Close modals on escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeTaskModal();
        closeMemberModal();
    }
});
