const editButtons = document.querySelectorAll(".edit_saved_search");
const deleteButtons = document.querySelectorAll(".delete_saved_search")


for (const button of editButtons) {
    button.addEventListener('click', () => {
        const listItem = button.closest('.parent_li');
        const searchNameInput = listItem.querySelector('.search_name_input');
        const searchId = searchNameInput.dataset.searchId;
        const newNickname = searchNameInput.value;

    fetch(`/edit_saved_search/${searchId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({newNickname})
    })
    .then((response) => {console.log(response); return response.json()})
    .then((data) => {
        console.log('RESPONSE DATA', data)
        if (data.success) {
            const successMessage = document.getElementById(`successMessage_${searchId}`);
            successMessage.innerHTML = "Search name updated successfully!";
            const searchNameDisplay = listItem.querySelector('.search_name_display');
            searchNameDisplay.innerHTML = newNickname
        }
    })
    } )
}

for (const button of deleteButtons) {
    button.addEventListener('click', () => {
        const searchId = button.dataset.searchId;
        fetch(`/delete_saved_search/${searchId}`, {
            method: 'DELETE'
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                const successMessage = document.getElementById(`successMessage_${searchId}`);
                successMessage.innerHTML = "Search deleted!";
                const parentListItem = document.getElementById(`list_item_${searchId}`)
                parentListItem.style.display = 'none';

            }
        })

    })
}