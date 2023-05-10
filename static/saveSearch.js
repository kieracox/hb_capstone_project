document.addEventListener("DOMContentLoaded", () => {
    const saveSearchForm = document.querySelector(".save_search");
    saveSearchForm.addEventListener("submit", (event) => {
        event.preventDefault();
        const formData = new FormData(saveSearchForm);
        fetch("/save_search", {
            method: 'POST',
        body: formData 
        })
        .then((response) => response.json())
        .then((data) =>{
            const successDiv = document.querySelector('.success')
            const failureDiv = document.querySelector('.failure')
            const nicknameInput = saveSearchForm.querySelector("[name='search_nickname']");
            if (data.success) {
                saveSearchForm.style.display = 'none';
                successDiv.style.display = 'block';
            } else {
                failureDiv.style.display = 'block';
                nicknameInput.value = '';
            }
        });
    })
});