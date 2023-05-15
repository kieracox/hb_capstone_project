const removeButtons = document.querySelectorAll(".remove_connection")

for (const button of removeButtons) {
    button.addEventListener('click', () => {
        const removeId = button.dataset.id;
        const confirmRemove = confirm("Are you sure you want to remove this connection?");

        if (confirmRemove) {
        fetch(`/remove_connection/${removeId}`, {
            method: 'DELETE'
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                const successMessage = document.getElementById(`removeSuccessMessage_${removeId}`);
                successMessage.innerHTML = "Connection removed.";
                const parentListItem = document.getElementById(`connection_item_${removeId}`)
                parentListItem.style.display = 'none';

            }
        })
    }
    })
}