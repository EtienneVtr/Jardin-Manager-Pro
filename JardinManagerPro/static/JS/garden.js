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
    
  // Remise à zéro du menu déroulant
    document.getElementById('vegetable-select').selectedIndex = 0;



// Ajout d'un gestionnaire d'événement "click" à chaque cellule du tableau
var cells = document.querySelectorAll('td');
cells.forEach(function(cell) {
  cell.addEventListener('click', function(event) {
    // Récupère le légume sélectionné
    var vegetable = document.getElementById('vegetable-select').value;

    if (vegetable) {
      // Ajoute la classe correspondante à la cellule
      cell.classList.add(vegetable);
      // Ajoute le dégradé de vert à la cellule
      addVegetableBackground(cell);
    }else {
      // Supprime toutes les classes et le background de la cellule cliquée
      cell.className = "";
      cell.style.background = "";
    }
  });
});



// Variable qui indique si le mode suppression est activé ou non
var deleteMode = false;

// Gestionnaire d'événement pour le bouton "Supprimer case"
document.getElementById('delete-cell').addEventListener('click', function(event) {
  deleteMode = !deleteMode; // Inverse la valeur de deleteMode
  if (deleteMode) {
    event.target.textContent = 'Annuler suppression'; // Change le texte du bouton en "Annuler suppression"
    // Remise à zéro du menu déroulant
    document.getElementById('vegetable-select').selectedIndex = 0;
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

// Gestionnaire d'événement pour le bouton "Poubelle"
document.querySelector('.delete').addEventListener('click', function() {
  currentVegetable = null; // Remise à null de currentVegetable pour désélectionner le légume actuel
    // Remise à zéro du menu déroulant
    document.getElementById('vegetable-select').selectedIndex = 0;
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
    // Remise à zéro du menu déroulant
    document.getElementById('vegetable-select').selectedIndex = 0;
  // Suppression de toutes les classes "carrot" et "tomato" des cellules
  var cells = document.querySelectorAll('td');
  cells.forEach(function(cell) {
    cell.classList.remove('carrot');
    cell.classList.remove('tomato');
    cell.style.background = "";
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

//Fonction pour ajouter un fond de sable
function addPathBackground(cell) {
  cell.style.background = '#F4D35E';
}

  // Fonction qui ajoute un dégradé de vert à une cellule
  function addVegetableBackground(cell) {
    cell.style.background = 'linear-gradient(90deg, #9bcc50, #8bac40)';
  }







//SAUVEGARDER

function saveFile() {
  // Récupérez les données de configuration du tableau ici
  var data = getTableData();

  // Convertissez vos données de configuration en chaîne de caractères pour écrire dans le fichier
  var dataString = JSON.stringify(data);

  // Création d'un objet Blob à partir de la chaîne de caractères
  var file = new Blob([dataString], {type: 'text/plain'});

  // Création d'une URL qui pointe vers le fichier
  var fileUrl = URL.createObjectURL(file);

  // Création d'un lien HTML qui déclenchera le téléchargement du fichier lorsqu'il sera cliqué
  var link = document.createElement('a');
  link.setAttribute('download', 'jardin.txt'); // Nom du fichier
  link.setAttribute('href', fileUrl);
  link.click(); // Déclenchement du téléchargement

  // Suppression de la référence au fichier pour libérer de la mémoire
  URL.revokeObjectURL(fileUrl);
}



//Fonction qui permet de récupérer les données de configuration d'un tableau


function getTableData() {
  // Objet qui contiendra les données de configuration
  var data = {
    cells: [] // Tableau qui contiendra les données de chaque cellule
  };

  // Récupération de toutes les cellules du tableau
  var cells = document.querySelectorAll('td');

  // Parcours de chaque cellule du tableau
  cells.forEach(function(cell) {
    // Récupération de la ligne et de la colonne de la cellule
    var row = cell.parentNode.rowIndex;
    var col = cell.cellIndex;

    // Récupération du contenu de la cellule (légume, vide, etc.)
    var content = cell.innerHTML;

    // Enregistrement des informations de la cellule dans le tableau de données
    data.cells.push({
      row: row,
      col: col,
      content: content
    });
  });

  // Renvoi des données de configuration
  return data;
  
}


// Gestionnaire d'événements "click" pour le bouton "Sauvegarder"
document.getElementById('save-file').addEventListener('click', function() {
  // Appelez une fonction pour sauvegarder la configuration actuelle du tableau
  saveFile();
});


//CHARGER

// Gestionnaire d'événement pour la soumission du formulaire de chargement de fichier
document.getElementById('load-form').addEventListener('submit', function(event) {
  event.preventDefault(); // Empêche le formulaire de soumettre les données (recharge de la page)

  // Récupération du fichier sélectionné
  var fileInput = document.getElementById('load-file');
  var file = fileInput.files[0];

  // Lecture du contenu du fichier
  var reader = new FileReader();
  reader.onload = function() {
    // Le fichier a été lu, vous pouvez traiter son contenu ici
    var fileContent = reader.result;

    // Parsing du contenu du fichier
    var data = JSON.parse(fileContent);
    var width = data.width;
    var height = data.height;
    var vegetables = data.vegetables;

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
        cell.innerHTML = ""; // Case vide par défaut
        row.appendChild(cell);
      }
      table.appendChild(row);
    }

    // Remplissage de la grille avec les légumes enregistrés
    for (var i = 0; i < vegetables.length; i++) {
      var vegetable = vegetables[i];
      var row = vegetable.row;
      var col = vegetable.col;
      var content = vegetable.content;
      table.rows[row].cells[col].innerHTML = content;
    }

    // Ajout du tableau à la page HTML
    document.body.appendChild(table);
  };
  reader.readAsText(file);
});