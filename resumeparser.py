
import spacy  # natural language processing
import re
import os
import pandas as pd
import pdf2txt
import pdfminer


def convert_pdf(f):
    output_filename = os.path.basename(os.path.splitext(f)[0]) + ".txt"  # i.e. filename.pdf becomes ["filename", "pdf"] from which we use the first entry
    output_filepath: str = os.path.join('C:\\Users\\matt_\\PycharmProjects\\pythonProject\\ouput\\txt', output_filename)  # steckt die Datei in den Ordner txt
    pdf2txt.main(args=[f, "--outfile", output_filepath])  # pdf to text and save it in the given location, --outfile = output_filename
    print(output_filename + " saved successfully!")
    return open(output_filepath, encoding="utf8").read()


# load the language model with spacy

nlp = spacy.load("en_core_web_sm")

result_dict = {"name": [], "phone": [], "email": [], "skills": []}
names = []
phones = []
emails = []
skills = []


def parse_content(text):
    skillset = re.compile("python|java|sql|hadoop|tableau")
    phone_num = re.compile("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})")
    doc = nlp(text)
    name = [entity.text for entity in doc.ents if entity.label_ is "PERSON"][0]
    print(name)
    email = [word for word in doc if word.like_email == True][0]
    print(email)
    phone = str(re.findall(phone_num, text.lower()))
    skills_list = re.findall(skillset, text.lower())
    unique_skills_list = str(set(skills_list))
    names.append(name)
    emails.append(email)
    phones.append(phone)
    skills.append(unique_skills_list)
    print("Extraction completed successfully")


for file in os.listdir("C:\\Users\\matt_\\PycharmProjects\\pythonProject\\resumes"):
    if file.endswith(".pdf"):
        print("Reading....." + file)
        txt = convert_pdf(os.path.join("C:\\Users\\matt_\\PycharmProjects\\pythonProject\\resumes", file))
        parse_content(txt)

result_dict["name"] = names
result_dict["phone"] = phones
result_dict["email"] = emails
result_dict["skills"] = skills

result_df = pd.DataFrame(result_dict)
print(result_df)


result_df.to_csv("C:\\Users\\matt_\\PycharmProjects\\pythonProject\\ouput\\csv\\parsed_resumes.csv")