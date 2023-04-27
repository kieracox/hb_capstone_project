
const detailButtons = document.querySelectorAll('.show_details');

for (const button of detailButtons) {
    button.addEventListener('click', () => {
        const detailsDiv = document.querySelector(`#show_${button.id}`);
        if (detailsDiv !== null && detailsDiv.style.display === 'none') {
            detailsDiv.style.display = 'block';
            button.innerHTML = 'Hide Details';
        } else if (detailsDiv !== null) {
            detailsDiv.style.display = 'none';
            button.innerHTML = 'Show Details';
        }
    })
}