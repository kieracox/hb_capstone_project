document.addEventListener('DOMContentLoaded', () => {
    const notifications = document.querySelectorAll('.notifications');
    for (const notification of notifications) {
        notification.addEventListener('click', () => {
        const notificationID = notification.getAttribute('data-id');
        fetch(`mark_notification_read/${notificationID}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                notification.classList.add('read');
            } else {
                console.error(data.error);
            }
        })
        })
    }
})