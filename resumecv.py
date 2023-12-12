import streamlit as st
import pdfplumber
import spacy
from spacy.matcher import Matcher

def extraire_informations_cv(texte):
    nlp = spacy.load("fr_core_news_sm")
    matcher = Matcher(nlp.vocab)

    matcher.add("NOM", [[{"POS": "PROPN"}]])
    matcher.add("EMAIL", [[{"TEXT": {"REGEX": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"} }]])
    matcher.add("TELEPHONE", [[{"TEXT": {"REGEX": r"\b(?:0|\\+33|0033)[1-9][0-9]{8}\b"} }]])

    doc = nlp(texte)

    informations = {"Nom": "", "Email": "", "Téléphone": ""}

    for match_id, start, end in matcher(doc):
        if match_id == nlp.vocab.strings["NOM"]:
            informations["Nom"] = doc[start:end].text
        elif match_id == nlp.vocab.strings["EMAIL"]:
            informations["Email"] = doc[start:end].text
        elif match_id == nlp.vocab.strings["TELEPHONE"]:
            informations["Téléphone"] = doc[start:end].text

    return informations

def extraire_texte_pdf(pdf_file):
    #doc = fitz.open(pdf_file)
    texte_pdf = ""

    with pdfplumber.open(pdf_file) as pdf:
        texte = ""
        for page in pdf.pages:
            texte_pdf += page.extract_text()
    return texte_pdf

def main():
    st.title("Application d'extraction d'informations de CV")

    cv_file = st.file_uploader("Téléchargez votre CV (format .pdf)", type=["pdf"])

    if cv_file is not None:
        texte_cv = extraire_texte_pdf(cv_file)

        st.subheader("Texte brut du CV")
        st.text(texte_cv)

        informations = extraire_informations_cv(texte_cv)

        st.subheader("Informations extraites du CV")
        st.write(f"Nom: {informations['Nom']}")
        st.write(f"Email: {informations['Email']}")
        st.write(f"Téléphone: {informations['Téléphone']}")

if __name__ == "__main__":
    main()
