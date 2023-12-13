import PyPDF2
import re
import spacy
import pandas as pd

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def extract_information(text):
    # Expression régulière pour extraire l'email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)

    # Expression régulière pour extraire le numéro de téléphone
    phone_pattern = r'\b(?:\+\d{1,2}\s?)?(?:\(\d{1,4}\))?(?:\d{1,4}[-.\s]?){2,}\d{1,4}\b'
    phones = re.findall(phone_pattern, text)

    # Utilisation de spaCy pour l'analyse linguistique
    nlp = spacy.load('fr_core_news_sm')
    doc = nlp(text)

    # Extraction des entités nommées
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Filtrage des entités pertinentes (Nom, Prénom, Formation, Compétences)
    relevant_entities = [entity[0] for entity in entities if entity[1] in ['PER', 'ORG', 'LOC', 'MISC']]

    # Extraction du nom et prénom
    full_name = " ".join(relevant_entities)

    # Extraction de la formation (assumons que "Formation" est une entité pertinente)
    formation = " ".join([entity for entity in relevant_entities if "Formation" in entity])

    # Extraction des compétences (assumons que "Compétences" est une entité pertinente)
    competences = " ".join([entity for entity in relevant_entities if "Compétences" in entity])

    return {
        'emails': emails,
        'phones': phones,
        'full_name': full_name,
        'formation': formation,
        'competences': competences
    }

if __name__ == "__main__":
    pdf_path = "CV_N'DAH ETCHIAN ARNAUD-JOSE.pdf"
    text = extract_text_from_pdf(pdf_path)
    information = extract_information(text)

    print("Emails:", information['emails'])
    print("Téléphones:", information['phones'])
    print("Nom et Prénom:", information['full_name'])
    print("Formation:", information['formation'])
    print("Compétences:", information['competences'])

    # Création d'un DataFrame à partir des informations extraites
    df = pd.DataFrame([information])

    # Affichage du DataFrame
    print(df)