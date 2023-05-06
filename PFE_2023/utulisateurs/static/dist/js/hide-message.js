// Sélectionnez l'élément qui contient le message d'erreur
var errorElement = document.querySelector('.alert-danger');

// Si l'élément existe, ajoutez la classe 'hidden' après 1 minute
if (errorElement) {
  setTimeout(function() {
    errorElement.classList.add('hidden');
  }, 60000); // Durée en millisecondes (60 000 ms = 1 minute)
}

var successElement = document.querySelector('.alert-success');

// Si l'élément existe, ajoutez la classe 'hidden' après 1 minute
if (successElement) {
  setTimeout(function() {
    successElement.classList.add('hidden');
  }, 60000); // Durée en millisecondes (60 000 ms = 1 minute)
}
