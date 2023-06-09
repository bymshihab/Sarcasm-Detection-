document.getElementById('prediction-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    var sentences = document.getElementById('sentences').value;
    var predictions = document.getElementById('predictions');

    // Clear button functionality
    document.getElementById('clear-button').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default button behavior

        // Clear the textarea
        document.getElementById('sentences').value = '';
        // Clear the predictions
        document.getElementById('predictions').innerHTML = '';
    });

    // Make a POST request to the Flask endpoint for prediction
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ sentences: sentences })
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        // Display the prediction result
        var result = data.predictions[0] > 0.5 ? 'Sarcastic' : 'Non-sarcastic';
        predictions.innerHTML = 'Prediction: ' + result;
    })
    .catch(function(error) {
        console.error('Error:', error);
    });
});

document.getElementById('review-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    var review = document.getElementById('review').value;

    // Make a POST request to the Flask endpoint for adding a review
    fetch('/review', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ review: review })
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        // Display the success message
        alert(data.message);
        // Clear the review textarea
        document.getElementById('review').value = '';
    })
    .catch(function(error) {
        console.error('Error:', error);
    });
});
