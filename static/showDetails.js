
const detailButtons = document.querySelectorAll('.show_details');

for (const button of detailButtons) {
    button.addEventListener('click', () => {
        const roleId = button.id.replace('show_details_', '');
        const detailsDiv = document.querySelector(`#show_${roleId}`);
        if (detailsDiv !== null && detailsDiv.style.display === 'none') {
            detailsDiv.style.display = 'block';
            button.innerHTML = 'Hide Details';
        } else if (detailsDiv !== null) {
            detailsDiv.style.display = 'none';
            button.innerHTML = 'Show Details';
        }
    })
}

const editButtons = document.querySelectorAll('.show_edit');

for (const button of editButtons) {
    button.addEventListener('click', (event) => {
        event.preventDefault();
        const roleId = button.id.replace('edit_details_', '');
        const editDiv = document.querySelector(`#edit_${roleId}`);
        if (editDiv !== null && editDiv.style.display === 'none') {
            editDiv.style.display = 'block';
            button.innerHTML = 'Collapse Form';
        } else if (editDiv !== null) {
            editDiv.style.display = 'none';
            button.innerHTML = 'Show Edit Form';
        }
    })
}