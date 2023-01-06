// Gestionnaire d'événements "click" pour le bouton "Sauvegarder"
document.getElementById('save-file').addEventListener('click', function() {
    // Appelez une fonction pour sauvegarder la configuration actuelle du tableau
    saveFile();
  });
  
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
  
  // Gestionnaire d'événements "submit" pour le formulaire de chargement de fichier
  document.getElementById('load-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Empêche le formulaire de soumettre les données (recharge de la page)
  
    // Appelez une fonction pour charger le fichier sélectionné
    loadFile();
  });
  
  function loadFile() {
    // Récupération du fichier sélectionné par l'utilisateur
    var file = document.getElementById('load-file').files[0];
  
    // Vérification de la validité du fichier
    if (!file) {
      alert('Veuillez sélectionner un fichier à charger !'); // Affichage d'un message d'erreur
      return; // Arrêt de la fonction
    }
  
    // Création d'un objet FileReader pour lire le contenu du fichier
    var reader = new FileReader();
  
    // Ajout d'un gestionnaire d'événements "load" pour exécuter une fonction lorsque le fichier est chargé
    reader.addEventListener('load', function() {
      // Récupération des données de configuration du fichier sous forme de chaîne de caractères
      var dataString = reader.result;
  
      // Convertion de la chaîne de caractères en objet JavaScript
      var data = JSON.parse(dataString);
  
      
      // Suppression du tableau précédemment généré
      var table = document.querySelector('table');
      if (table) {
        table.parentNode.removeChild(table);
      }
  
      // Création d'un nouveau tableau HTML vide
      table = document.createElement('table');
  
      // Création des lignes et des colonnes du tableau
      for (var i = 0; i < data.height; i++) {
        var row = document.createElement('tr');
        for (var j = 0; j < data.width; j++) {
          var cell = document.createElement('td');
          cell.innerHTML = ""; // Case vide
          row.appendChild(cell);
        }
        table.appendChild(row);
      }
  
      // Ajout du tableau à la page HTML
      document.body.appendChild(table);
  
      // Remplissage du tableau avec les données de configuration
      data.cells.forEach(function(cellData) {
        // Récupération de la cellule correspondante
        var cell = table.rows[cellData.row].cells[cellData.col];
  
        // Mise à jour du contenu de la cellule
        cell.innerHTML = cellData.content;
      });
  
      // Affichez les boutons de la barre d'outils
      document.getElementById('button-container').style.display = 'block';
    });
  
    // Lecture du fichier sélectionné par l'utilisateur
    reader.readAsText(file);
  }
  
  
  
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
  








  CHARGER : 
  // Gestionnaire d'événements "submit" pour le formulaire de chargement de fichier
document.getElementById('load-form').addEventListener('submit', function(event) {
  event.preventDefault(); // Empêche le formulaire de soumettre les données (recharge de la page)

  // Appelez une fonction pour charger le fichier sélectionné
  loadFile();
});

function loadFile() {
  // Récupération du fichier sélectionné par l'utilisateur
  var file = document.getElementById('load-file').files[0];

  // Vérification de la validité du fichier
  if (!file) {
    alert('Veuillez sélectionner un fichier à charger !'); // Affichage d'un message d'erreur
    return; // Arrêt de la fonction
  }

  // Création d'un objet FileReader pour lire le contenu du fichier
  var reader = new FileReader();

  // Ajout d'un gestionnaire d'événements "load" pour exécuter une fonction lorsque le fichier est chargé
  reader.addEventListener('load', function() {
    // Récupération des données de configuration du fichier sous forme de chaîne de caractères
    var dataString = reader.result;

    // Convertion de la chaîne de caractères en objet JavaScript
    var data = JSON.parse(dataString);

    // Gestion d'erreur en cas d'échec de la conversion
    if (!data) {
      alert('Le fichier sélectionné n\'est pas valide !');
      return;
    }

    var table;
    // Suppression du tableau précédemment généré
    var table = document.querySelector('table');
    if (table) {
      table.parentNode.removeChild(table);
    }
    
    // Création d'un nouveau tableau HTML vide
    table = document.createElement('table');
    
    // Création des lignes et des colonnes du tableau
    for (var i = 0; i < data.height; i++) {
      var row = document.createElement('tr');
      for (var j = 0; j < data.width; j++) {
        var cell = document.createElement('td');
        cell.innerHTML = ""; // Case vide
        row.appendChild(cell);
      }
      table.appendChild(row);
    }
    
    // Ajout du tableau à la page HTML
    document.body.appendChild(table);

     // Remplissage du tableau avec les données de configuration
     data.cells.forEach(function(cellData) {
      // Récupération de la cellule correspondante, si elle existe
      if (cellData.row < table.rows.length && cellData.col < table.rows[cellData.row].cells.length) {
        var cell = table.rows[cellData.row].cells[cellData.col];
        // Mise à jour du contenu de la cellule
        cell.innerHTML = cellData.content;
        
      }
    });

    // Affichez les boutons de la barre d'outils
    document.getElementById('button-container').style.display = 'block';
  });

  // Lecture du fichier sélectionné par l'utilisateur
  
  reader.readAsText(file);
}

