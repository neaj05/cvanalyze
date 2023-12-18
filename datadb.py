import PyPDF2
import re
import sqlite3

# Fonction pour extraire les informations du CV PDF
def extraire_informations_cv_pdf(chemin_cv_pdf):
    # Ouvrir le fichier PDF
    with open(chemin_cv_pdf, 'rb') as fichier_pdf:
        # Utiliser PyPDF2 pour lire le contenu du PDF
        lecteur_pdf = PyPDF2.PdfReader(fichier_pdf)

        # Initialiser une chaîne pour stocker le texte extrait du PDF
        texte_cv = ""

        # Parcourir toutes les pages du PDF et extraire le texte
        for num_page in range(len(lecteur_pdf.pages)):
            texte_cv += lecteur_pdf.pages[num_page].extract_text()

    # Implémenter la logique pour extraire les différentes informations du CV
    # (Nom, Prénom, Email, Téléphone, Éducation, Expérience, Compétences, Langues, etc.)
    nom = re.search(r'Nom\s*:\s*([^\n]+)', texte_cv).group(1) if re.search(r'Nom\s*:\s*([^\n]+)', texte_cv) else None
    prenom = re.search(r'Prénom\s*:\s*([^\n]+)', texte_cv).group(1) if re.search(r'Prénom\s*:\s*([^\n]+)', texte_cv) else None
    email = re.search(r'Email\s*:\s*([^\n]+)', texte_cv).group(1) if re.search(r'Email\s*:\s*([^\n]+)', texte_cv) else None
    telephone = re.search(r'Tél\s*:\s*([^\n]+)', texte_cv).group(1) if re.search(r'Tél\s*:\s*([^\n]+)', texte_cv) else None
    competence = re.search(r'Compétences\s*:\s*([^\n]+)', texte_cv).group(1) if re.search(r'Compétences\s*:\s*([^\n]+)', texte_cv) else None
    formation = re.search(r'Formation\s*:\s*([^\n]+)', texte_cv).group(1) if re.search(r'Formation\s*:\s*([^\n]+)', texte_cv) else None
    # Ajoutez d'autres informations extraites du CV

    # Retourner un dictionnaire avec les informations extraites
    informations = {
        'Nom': nom,
        'Prenom': prenom,
        'Email': email,
        'Telephone': telephone,
        'Competence': competence,
        'Formation' : formation,
        # Ajoutez d'autres informations extraites du CV
    }

    return informations

def initialiser_base_de_donnees():
    conn = sqlite3.connect("cvdb.db")
    cursor = conn.cursor()

    # Créer une table pour stocker les informations d'identification des utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Candidats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nom TEXT,
            Prenom TEXT,
            Email TEXT,
            Telephone TEXT,
            Competence TEXT,
            Formation TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Fonction pour insérer les informations dans la base de données SQLite
def inserer_dans_base_de_donnees(informations):
    # Connexion à la base de données SQLite (si elle n'existe pas, elle sera créée)
    conn = sqlite3.connect('cvdb.db')
    cursor = conn.cursor()

    # Insérer les informations du candidat dans la table "Candidats"
    cursor.execute("INSERT INTO Candidats (Nom, Prenom, Email, Telephone, Competence, Formation) VALUES (?, ?, ?, ?, ?, ?)",
                   (informations['Nom'], informations['Prenom'], informations['Email'], informations['Telephone'], informations['Competence'], informations['Formation']))
    conn.commit()

    # Récupérer l'ID du candidat inséré
    cursor.execute("SELECT last_insert_rowid()")
    id = cursor.fetchone()[0]

    # Insérer d'autres informations dans les tables correspondantes (Éducation, Expérience, Compétences, Langues, etc.)
    # (Adaptez cette partie en fonction de la structure réelle de votre CV)

    # Fermer la connexion à la base de données
    conn.close()

# Exemple d'utilisation
chemin_du_cv_pdf = "CV_N'DAH ETCHIAN ARNAUD-JOSE.pdf"
informations_cv_pdf = extraire_informations_cv_pdf(chemin_du_cv_pdf)
initialiser_base_de_donnees()
inserer_dans_base_de_donnees(informations_cv_pdf)
print(informations_cv_pdf)