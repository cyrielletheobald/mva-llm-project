import ollama
from src.dataprep import get_prompt_patient_data, system
from src.config import PROMPT_SYSTEM,  PROMPT_MODEL_EXPERT 
import re 
import pandas as pd
import os
import re 
import subprocess 
import pandas as pd 
from src.config import PATH_PROJECT
from langchain.document_loaders import PyMuPDFLoader
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

df = pd.read_excel(os.path.join(PATH_PROJECT, "data/") + "dataset.xlsx").fillna("Non renseigné")
### LLM SOLO 


def get_answer(patient_id, model='mistral'):
    observed, history_conditions, mood_episodes = get_prompt_patient_data(patient_id) 
    user = f'For brevity, please output only the diagnosis for the following patients. Patients with no clear diagnosis should be indicated as such. {observed}, {history_conditions}'
    response = ollama.chat(
    model=model,
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ])
    return response['message'].content

#---
### LLM WITH LOGICAL PROGRAMMING
#---

from src import code_Datalog
import os
import subprocess

### traitement des réponses 

def traitement_reponse(ollama_output, nom_model = None, nom_model_expert = None, lan_logic = 'Datalog'):
    # Extraction du bloc <explanation>...</explanation>
    explanation_match = re.search(r"<explanation>(.*?)</explanation>", ollama_output, re.DOTALL)
    explanation = explanation_match.group(1).strip() if explanation_match else None

    # Extraction du bloc <code>...</code>
    code_match = re.search(r"<code>(.*?)</code>", ollama_output, re.DOTALL)
    code = code_match.group(1).strip() if code_match else None
    if code:
        with open(f"code_{lan_logic}_{nom_model}_{nom_model_expert}.py", "w") as f:
            f.write(code)
    if explanation :
        with open(f'explanation__{lan_logic}_{nom_model}_{nom_model_expert}.txt', 'w') as f : 
            f.write(explanation)
    return(code)

def traitement_reponse_expert(ollama_output, nom_model = None, nom_model_expert = None, lan_logic = 'Datalog'):
    # Extraction du bloc <explanation>...</explanation>
    explanation_match = re.search(r"<rep>(.*?)</rep>", ollama_output, re.DOTALL)
    explanation = explanation_match.group(1).strip() if explanation_match else None

    # Extraction du bloc <code>...</code>
    code_match = re.search(r"<code>(.*?)</code>", ollama_output, re.DOTALL)
    code = code_match.group(1).strip() if code_match else None
    if code:
        with open(f"code_{lan_logic}_corr_{nom_model}_{nom_model_expert}.py", "w") as f:
            f.write(code)
    if explanation :
        with open(f'explanation_expert_{lan_logic}_{nom_model}_{nom_model_expert}.txt', 'w') as f : 
            f.write(explanation)


### génération du code par les modèles 

def get_code(model = 'deepseek-coder-v2', model_expert = 'deepseek-coder-v2', w_model_expert = True, prompt_system = PROMPT_SYSTEM, prompt_system_expert = PROMPT_MODEL_EXPERT, lan_logic = 'Datalog') : 
    user = f'''Now, translate the following criteria into python code WITH THE PACKAGE pyDatalog for Bipolar I, Bipolar II, Single Episode Depressive Disorder, and
Recurrent Depressive Disorder. IT MUST BE IN PYTHON WITH THE PACKAGE pyDatalog.
• Mood Episode criterion: [Depressive, Manic, Mixed, and Hypomanic Episode criteria from ICD-11 CDDR].
• Mood Disorder criterion: [Bipolar I, Bipolar II, Single Episode Depressive Disorder, and Recurrent Depressive Disorder criteria
from ICD-11 CDDR].
• Relevant symptom names for Observed relation: [Symptom names]
• Relevant condition names for History relation: [Condition names]'''
    response = ollama.chat(
    model=model,
    messages=[
        {"role": "system", "content": prompt_system},
        {"role": "user", "content": user}
    ])
    if w_model_expert == False: 
        code = traitement_reponse(response['message'].content, model, 'without_expert', lan_logic)
    else : 
        code = traitement_reponse(response['message'].content, model, model_expert, lan_logic)
        assert isinstance(model_expert, str)
        check_expert(model, model_expert, code, prompt_system_expert, lan_logic)

def get_code_with_rag(model = 'deepseek-coder-v2', model_expert = 'deepseek-coder-v2', w_model_expert = True, prompt_system = PROMPT_SYSTEM, prompt_system_expert = PROMPT_MODEL_EXPERT, lan_logic = 'Datalog') : 
    
    vectorstore = get_vectorstore()
    # Step 1: Retrieve relevant ICD-11 CDDR diagnostic criteria using RAG
    disorders = ['Bipolar I', 'Bipolar II', 'Single Episode Depressive Disorder', 'Recurrent Depressive Disorder']
    retrieved_contexts = []

    for disorder in disorders:
        query = f"What are the diagnostic criteria for {disorder}?"
        retrieved_docs = vectorstore.similarity_search(query, k=3)  # Retrieve top 3 most relevant documents
        retrieved_context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        retrieved_contexts.append(f"### {disorder}:\n{retrieved_context}")

    retrieved_context = "\n\n".join(retrieved_contexts) 
    
    # Step 2: Construct user query with retrieved context
    user = f'''Now, translate the following criteria into python code WITH THE PACKAGE pyDatalog for Bipolar I, Bipolar II, Single Episode Depressive Disorder, and
    Recurrent Depressive Disorder. IT MUST BE IN PYTHON WITH THE PACKAGE pyDatalog.

    {retrieved_context}
    • Relevant symptom names for Observed relation: [Symptom names]
    • Relevant condition names for History relation: [Condition names]'''
    
    response = ollama.chat(
    model=model,
    messages=[
        {"role": "system", "content": prompt_system},
        {"role": "user", "content": user}
    ])
    if w_model_expert == False: 
        code = traitement_reponse(response['message'].content, model, 'without_expert', lan_logic)
    else : 
        code = traitement_reponse(response['message'].content, model, model_expert, lan_logic)
        assert isinstance(model_expert, str)
        check_expert(model, model_expert, code, prompt_system_expert, lan_logic)

def get_vectorstore() :
    CHROMA_PERSIST_DIR = os.path.join(PATH_PROJECT, "data/chroma_db/")

    if not os.path.exists(CHROMA_PERSIST_DIR) or not os.listdir(CHROMA_PERSIST_DIR):
        print("🆕 Création de la base Chroma et indexation des documents...")

        # Charger les fichiers PDF
        data_dir = os.path.join(PATH_PROJECT, "data/")
        documents = []

        for file in os.listdir(data_dir):
            if file.endswith(".pdf"):
                pdf_path = os.path.join(data_dir, file)
                pdf_loader = PyMuPDFLoader(pdf_path)
                documents.extend(pdf_loader.load())

        # Diviser les documents en chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.split_documents(documents)

        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2",
                                        model_kwargs={'device': device}, encode_kwargs={'device': device})

        # Initialiser Chroma avec les embeddings 
        vectorstore = Chroma.from_documents(docs, embedding_model, persist_directory=CHROMA_PERSIST_DIR)
        vectorstore.persist()
        print("Base Chroma sauvegardée avec succès")

    else:
        print("Chargement de la base Chroma existante...")
        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2",
                                        model_kwargs={'device': device}, encode_kwargs={'device': device})
        vectorstore = Chroma(persist_directory=CHROMA_PERSIST_DIR, embedding_function=embedding_model)

    print("Base Chroma prête à être utilisée")
    return vectorstore

def check_expert(model = 'deepseek-coder-v2', model_expert = 'deepseek-coder-v2', code = '', prompt_system_expert = PROMPT_MODEL_EXPERT, lan_logic = 'Datalog'):
    if model_expert == None :
        model_expert = model
    response = ollama.chat(
    model=model_expert,
    messages=[
        {"role": "system", "content": 
prompt_system_expert},
        {"role": "user", "content": code}
    ])
    traitement_reponse_expert(response['message'].content, model, model_expert, lan_logic)


### tester le code avec les patients id 

def get_prompt_patient_data_for_datalog(patient_id):
    patient_data = df[df['PatientID'] == patient_id]
    
    # Header
    lines = [
        "import sys",
        "sys.path.append('../')",
        "from notebooks import code_Datalog_corr",
        "",
        "pyDatalog.create_terms('X')",
        "",
        f"# Inject facts for patient {patient_id}"
    ]
    
    # Inject Observed
    for symptom, value in zip(patient_data["Observed_Symptom"].values.tolist(), patient_data["Obserrved_Week"].values.tolist()):
        lines.append(f"    + code_Datalog.Observed('{patient_id}', '{symptom}', {value})")
    
    # Inject History (si nécessaire)
    for condition, count in zip(patient_data["History_Condition"].values.tolist(), patient_data["History_Count"].values.tolist()):
        if condition != "Non renseigné":
            lines.append(f"    + code_Datalog.Observed('{patient_id}', '{condition}', {count})")
    
    # Query + Save Results
    lines += [
        "",
        "# Diagnosis Query",
        "results = code_Datalog.Diagnosis(code_Datalog.PATIENT, X).data",
        "",
        "# Save to txt",
        "with open('diagnosis_output.txt', 'w') as f:",
        "    for r in results:",
        f"        f.write(f'Patient {patient_id} : r[1]\\n')"
    ]
    
    # Sauvegarder le fichier Python
    output_file = f'patient_{patient_id}_diagnosis.py'
    with open(output_file, 'w') as f:
        f.write('\n'.join(lines))
    
    # Exécuter le script
    subprocess.run(['python', output_file], check=True)