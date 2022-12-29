// Gestionnaire d'événement pour la soumission du formulaire
document.getElementById('form').addEventListener('submit', function(event) {
  event.preventDefault(); // Empêche le formulaire de soumettre les données (recharge de la page)

  // Récupération des valeurs de largeur et de hauteur du formulaire
  var width = document.getElementById('width').value;
  var height = document.getElementById('height').value;

  // Vérification de la validité du formulaire
  if (width == '' || height == '') {
    alert('Veuillez remplir tous les champs !'); // Affichage d'un message d'erreur
    return; // Arrêt de la fonction
  }
  if (width > 25 || height > 25) {
    alert('La grille ne peut pas dépasser 25 par 25 !'); // Affichage d'un message d'erreur
    return; // Arrêt de la fonction
  }

  // Suppression du tableau précédemment généré
  var table = document.querySelector('table');
  if (table) {
    table.parentNode.removeChild(table);
  }

  // Création d'un tableau HTML vide
  table = document.createElement('table');

  // Création des lignes et des colonnes du tableau
  for (var i = 0; i < height; i++) {
    var row = document.createElement('tr');
    for (var j = 0; j < width; j++) {
      var cell = document.createElement('td');
      cell.innerHTML = ""; // Case vide
      row.appendChild(cell);
    }
    table.appendChild(row);
  }

  // Ajout du tableau à la page HTML
  document.body.appendChild(table);

  //affichage button
  document.getElementById('button-container').style.display = 'block';

  // Ajout d'un gestionnaire d'événement "click" à chaque cellule du tableau
  var cells = document.querySelectorAll('td');
  cells.forEach(function(cell) {
    cell.addEventListener('click', addVegetableClass);
  });
// Variable qui indique si le mode suppression est activé ou non
var deleteMode = false;

// Gestionnaire d'événement pour le bouton "Supprimer case"
document.getElementById('delete-cell').addEventListener('click', function(event) {
  deleteMode = !deleteMode; // Inverse la valeur de deleteMode
  if (deleteMode) {
    event.target.textContent = 'Annuler suppression'; // Change le texte du bouton en "Annuler suppression"
    // Réinitialise le menu déroulant
    document.getElementById('vegetable-select').form.reset();
  } else {
    event.target.textContent = 'Supprimer case'; // Change le texte du bouton en "Supprimer case"
  }
});

// Gestionnaire d'événement pour le menu déroulant
document.getElementById('vegetable-select').addEventListener('change', function(event) {
  // Annule le mode "Supprimer case"
  deleteMode = false;
  document.getElementById('delete-cell').textContent = 'Supprimer case';
});

// Gestionnaire d'événement pour chaque cellule du tableau
var cells = document.querySelectorAll('td');
cells.forEach(function(cell) {
  cell.addEventListener('click', function(event) {
    if (deleteMode) {
      // Supprime la cellule
      cell.parentNode.removeChild(cell);
    }
  });
});

});



// Variable globale pour stocker le légume actuellement sélectionné
var currentVegetable = null;

// Gestionnaire d'événement pour le menu déroulant
document.getElementById('vegetable-select').addEventListener('change', function(event) {
  // Mise à jour de currentVegetable avec le nom du légume sélectionné
  currentVegetable = event.target.value; 
  var selectedCells = document.querySelectorAll('.selected');
selectedCells.forEach(function(cell) {
  cell.classList.add('planted');
});
  // Mise à jour du gestionnaire d'événement "click" de chaque cellule
  var cells = document.querySelectorAll('td');
  cells.forEach(function(cell) {
    cell.removeEventListener('click', addVegetableClass);
    cell.addEventListener('click', addVegetableClass);
    
  });
});


 // Récupération de l'élément HTML du bouton "Réinitialiser"
var resetButton = document.getElementById('reset');
// Gestionnaire d'événement pour le bouton "Réinitialiser"
resetButton.addEventListener('click', function() {
  // Suppression du tableau précédemment généré
  var table = document.querySelector('table');
  if (table) {
    table.parentNode.removeChild(table);
  }
  // Réinitialisation de la valeur des champs de formulaire
  document.getElementById('width').value = '';
  document.getElementById('height').value = '';
  // Masquage des boutons
  document.getElementById('button-container').style.display = 'none';
});


// Fonction pour ajouter une classe CSS à une cellule en fonction de currentVegetable
function addVegetableClass(event) {
  // Récupération de la cellule ciblée par l'événement "click"
  var cell = event.target;

  // Suppression de toutes les classes CSS existantes de la cellule
  cell.className = '';

  // Ajout de la classe CSS correspondant à currentVegetable
  cell.classList.add(currentVegetable);
}

// Gestionnaire d'événement pour le bouton "Effacer"
document.querySelector('.delete').addEventListener('click', function() {
  currentVegetable = null; // Remise à null de currentVegetable pour désélectionner le légume actuel

  // Mise à jour du gestionnaire d'événement "click" de chaque cellule
  var cells = document.querySelectorAll('td');
  cells.forEach(function(cell) {
    cell.removeEventListener('click', addVegetableClass);
    cell.addEventListener('click', removeVegetableClass);
  });
});




// Gestionnaire d'événement pour le bouton "Effacer tout"
document.querySelector('.clear-all').addEventListener('click', function() {
  // Réinitialisation de currentVegetable
  currentVegetable = null;

  // Suppression de toutes les classes "carrot" et "tomato" des cellules
  var cells = document.querySelectorAll('td');
  cells.forEach(function(cell) {
    cell.classList.remove('carrot');
    cell.classList.remove('tomato');
  });
});



// Fonction pour ajouter une classe à la case sur laquelle l'utilisateur clique
function addVegetableClass() {
  this.classList.add(currentVegetable); // Ajout de la classe à la cellule sur laquelle l'utilisateur a cliqué
}

// Fonction pour effacer la classe de la case sur laquelle l'utilisateur clique
function removeVegetableClass() {
  this.className = ""; // Effacement de la classe de la cellule sur laquelle l'utilisateur a cliqué
}

