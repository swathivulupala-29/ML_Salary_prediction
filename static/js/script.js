document.getElementById("prediction-form").addEventListener("submit", function(event) {
    event.preventDefault();
    
    let formData = new FormData(this);

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("result").textContent = "Error: " + data.error;
        } else {
            document.getElementById("result").textContent = "$" + data.predicted_salary;
        }
    })
    .catch(error => console.error("Error:", error));
});
