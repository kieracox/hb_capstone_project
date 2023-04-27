const requestForms = document.querySelectorAll(".connect_form");

for (const form of requestForms) {
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        fetch("/send_connect", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const successDiv = document.querySelector(`#success_${form.id}`);
            form.style.display = 'none';
            successDiv.style.display = 'block';
            window.location.href= '/search'
        });
    })
    .catch(error => console.error(error));
}