import spacy
import PyPDF2
from sklearn.metrics import classification_report

# Charger le modèle NER pré-entraîné de spaCy
nlp = spacy.load("fr_core_news_sm")

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

# Exemple de texte CV (à remplacer par le texte réel)
pdf_path = "CV_N'DAH ETCHIAN ARNAUD-JOSE.pdf"
texte_cv = extract_text_from_pdf(pdf_path)

# Traitement du texte avec spaCy
doc = nlp(texte_cv)

# Annotations manuelles pour évaluation (à ajuster selon votre texte)
annotations = {
    "Jean Dupont": "NOM ET PRENOMS",
    "07 23 45 67 89": "TELEPHONE",
    "jean.dupont@email.com": "EMAIL",
    "Adinistrateur base de données": "POSTE",
    "Analyse de données": "POSTE",
    "Python, Java": "LANGAGE",
    "Elève Ingénieur, Première année": "FORMATION",
    "MySQL, SQL Server, MongoDB": "COMPETENCE",
    "PECB, Bioforce ,GOMYCODE": "CERTIFCATION",
}

# Extraction des entités prédites par spaCy
entites_predites = {ent.text: ent.label_ for ent in doc.ents}

# Création des listes pour évaluation
annotations_reelles = []
annotations_predites = []

# Remplissage des listes avec les annotations réelles et prédites
for texte, entite in annotations.items():
    annotations_reelles.append(entite)
    if texte in entites_predites:
        annotations_predites.append(entites_predites[texte])
    else:
        annotations_predites.append("")

# Évaluation des performances avec classification_report
rapport_classification = classification_report(annotations_reelles, annotations_predites)

print(doc)

# Affichage du rapport de classification
print(rapport_classification)
