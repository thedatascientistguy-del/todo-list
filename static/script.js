async function toggleTodo(todoId) {
    try {
        const response = await fetch(`/update/${todoId}`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const todoItem = document.querySelector(`[data-id="${todoId}"]`);
            todoItem.classList.toggle('completed');
            const toggleBtn = todoItem.querySelector('.toggle-btn');
            toggleBtn.textContent = todoItem.classList.contains('completed') ? 'Undo' : 'Complete';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function deleteTodo(todoId) {
    try {
        const response = await fetch(`/delete/${todoId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            const todoItem = document.querySelector(`[data-id="${todoId}"]`);
            todoItem.remove();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}