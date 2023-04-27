
document.addEventListener('DOMContentLoaded', () => {
const requestForms = document.querySelectorAll(".connect_form");
console.log(requestForms)
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
            console.log('Response from server:', data);
            const successDiv = document.querySelector(`#success_${formData.get("requested_id")}`);
            const failureDiv = document.querySelector(`#failure_${formData.get("requested_id")}`)
            console.log('Success div:', successDiv);
            form.style.display = 'none';
            if (data.success) {

                successDiv.style.display = 'block';
            } else {
                failureDiv.style.display = 'block';
            }
        });
    })
}
});