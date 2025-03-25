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
from src import dataprep
from tqdm import tqdm
import torch

device="cuda" if torch.cuda.is_available() else "cpu"

df = pd.read_excel(os.path.join(PATH_PROJECT, "data/") + "dataset.xlsx").fillna("Non renseigne")
df_grouped = dataprep.preproc_df()

device="cuda" if torch.cuda.is_available() else "cpu"


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


import os
import subprocess
from src.config import PATH_PROJECT
from langchain.document_loaders import PyMuPDFLoader
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

### traitement des réponses 

# Process the LLM output from the standard model.
# Extracts <explanation> and <code> blocks, saves them to files, and returns the code.

def traitement_reponse(ollama_output, nom_model=None, nom_model_expert=None, lan_logic='Datalog'):
    # Extract <explanation> block
    explanation_match = re.search(r"<explanation>(.*?)</explanation>", ollama_output, re.DOTALL)
    explanation = explanation_match.group(1).strip() if explanation_match else None

    # Extract <code> block
    code_match = re.search(r"<code>(.*?)</code>", ollama_output, re.DOTALL)
    code = code_match.group(1).strip() if code_match else None

    # Save code to file
    if code:
        with open(f"code_{lan_logic}_{nom_model}_{nom_model_expert}.py", "w") as f:
            f.write(code)
    
    # Save explanation to file
    if explanation:
        with open(f'explanation_{lan_logic}_{nom_model}_{nom_model_expert}.txt', 'w') as f:
            f.write(explanation)

    return code


# Process the LLM output from the expert model.
# Extracts <rep> and <code> blocks, saves them to files, and returns nothing.

def traitement_reponse_expert(ollama_output, nom_model=None, nom_model_expert=None, lan_logic='Datalog'):
    # Extract <rep> block
    explanation_match = re.search(r"<rep>(.*?)</rep>", ollama_output, re.DOTALL)
    explanation = explanation_match.group(1).strip() if explanation_match else None

    # Extract <code> block
    code_match = re.search(r"<code>(.*?)</code>", ollama_output, re.DOTALL)
    code = code_match.group(1).strip() if code_match else None

    # Save corrected code to file
    if code:
        with open(f"code_{lan_logic}_corr_{nom_model}_{nom_model_expert}.py", "w") as f:
            f.write(code)
    
    # Save expert explanation to file
    if explanation:
        with open(f'explanation_expert_{lan_logic}_{nom_model}_{nom_model_expert}.txt', 'w') as f:
            f.write(explanation)

# Generate logic code from LLM models using pyDatalog or other logical programming language and expert validation.
mood_criteria = """
Mood Episode Criteria (ICD-11 CDDR):

1. Depressive Episode:
   - Persistent depressed mood or loss of pleasure most of the day, nearly every day, for at least 2 weeks.
   - Accompanied by other cognitive, behavioral, or neurovegetative symptoms such as:
     - Reduced concentration or attention,
     - Feelings of worthlessness or excessive guilt,
     - Hopelessness,
     - Thoughts of death or suicidal ideation,
     - Insomnia or hypersomnia,
     - Significant weight change or appetite disturbance,
     - Psychomotor agitation or retardation,
     - Fatigue or loss of energy.
   - Must cause significant impairment in functioning or distress.
   - Not better explained by other disorders or physiological effects of substances.

2. Manic Episode:
   - Elevated, expansive, or irritable mood plus increased energy or activity lasting at least 1 week (or any duration if hospitalization is necessary).
   - Includes at least 3 of the following (4 if mood is only irritable):
     - Inflated self-esteem or grandiosity,
     - Decreased need for sleep,
     - More talkative or pressured speech,
     - Flight of ideas or racing thoughts,
     - Distractibility,
     - Increased goal-directed activity or psychomotor agitation,
     - Risky behaviors (e.g., spending sprees, risky sexual behavior).
   - Must cause significant functional impairment or necessitate hospitalization or be accompanied by psychotic symptoms.

3. Mixed Episode:
   - Rapidly alternating or simultaneous presence of manic and depressive symptoms.
   - Significant impairment in functioning or accompanied by delusions/hallucinations.
   - Not attributable to substances or medical conditions.

4. Hypomanic Episode:
   - Elevated or irritable mood and increased activity or energy lasting at least several days (typically ≥ 4 days).
   - Includes at least 3 of the manic symptoms (as above).
   - Less severe than a manic episode (no psychotic symptoms, hospitalization, or marked impairment required).
   - Represents a noticeable change from usual functioning.

Mood Disorder Criteria (ICD-11 CDDR):

1. Bipolar I Disorder:
   - History of at least one manic or mixed episode.
   - Typically alternates with depressive episodes.
   - Hypomanic episodes may occur but are not required.

2. Bipolar II Disorder:
   - History of at least one hypomanic episode and at least one depressive episode.
   - No history of manic or mixed episodes.

3. Single Episode Depressive Disorder:
   - A single depressive episode meeting all criteria for a depressive episode.
   - No history of manic, hypomanic, or mixed episodes.

4. Recurrent Depressive Disorder:
   - At least two depressive episodes, separated by periods of remission (i.e., no significant mood disturbance for several months).
   - No history of manic, hypomanic, or mixed episodes.
"""

def get_code(model='deepseek-coder-v2', model_expert='deepseek-coder-v2', w_model_expert=True, prompt_system=PROMPT_SYSTEM, prompt_system_expert=PROMPT_MODEL_EXPERT, lan_logic='Datalog'):
    # User prompt for initial model
    user = f'''Now, translate the following criteria into code for Bipolar I, Bipolar II, Single Episode Depressive Disorder, and
Recurrent Depressive Disorder. Implement the logical rules to determine the diagnosis. Careful, the patients are duplicated across lines for each observed symptom
• Mood Episode criterion: 1. Depressive Episode:
   - Persistent depressed mood or loss of pleasure most of the day, nearly every day, for at least 2 weeks.
   - Accompanied by other cognitive, behavioral, or neurovegetative symptoms such as:
     - Reduced concentration or attention,
     - Feelings of worthlessness or excessive guilt,
     - Hopelessness,
     - Thoughts of death or suicidal ideation,
     - Insomnia or hypersomnia,
     - Significant weight change or appetite disturbance,
     - Psychomotor agitation or retardation,
     - Fatigue or loss of energy.
   - Must cause significant impairment in functioning or distress.
   - Not better explained by other disorders or physiological effects of substances.

2. Manic Episode:
   - Elevated, expansive, or irritable mood plus increased energy or activity lasting at least 1 week (or any duration if hospitalization is necessary).
   - Includes at least 3 of the following (4 if mood is only irritable):
     - Inflated self-esteem or grandiosity,
     - Decreased need for sleep,
     - More talkative or pressured speech,
     - Flight of ideas or racing thoughts,
     - Distractibility,
     - Increased goal-directed activity or psychomotor agitation,
     - Risky behaviors (e.g., spending sprees, risky sexual behavior).
   - Must cause significant functional impairment or necessitate hospitalization or be accompanied by psychotic symptoms.

3. Mixed Episode:
   - Rapidly alternating or simultaneous presence of manic and depressive symptoms.
   - Significant impairment in functioning or accompanied by delusions/hallucinations.
   - Not attributable to substances or medical conditions.

4. Hypomanic Episode:
   - Elevated or irritable mood and increased activity or energy lasting at least several days (typically ≥ 4 days).
   - Includes at least 3 of the manic symptoms (as above).
   - Less severe than a manic episode (no psychotic symptoms, hospitalization, or marked impairment required).
   - Represents a noticeable change from usual functioning.
.
• Mood Disorder criterion: 1. Bipolar I Disorder:
   - History of at least one manic or mixed episode.
   - Typically alternates with depressive episodes.
   - Hypomanic episodes may occur but are not required.

2. Bipolar II Disorder:
   - History of at least one hypomanic episode and at least one depressive episode.
   - No history of manic or mixed episodes.

3. Single Episode Depressive Disorder:
   - A single depressive episode meeting all criteria for a depressive episode.
   - No history of manic, hypomanic, or mixed episodes.

4. Recurrent Depressive Disorder:
   - At least two depressive episodes, separated by periods of remission (i.e., no significant mood disturbance for several months).
   - No history of manic, hypomanic, or mixed episodes.
 Relevant symptom names for Observed relation: {df['Observed_Symptom'].unique()} Relevant condition names for History relation: {df['History_Condition'].unique()} Name of the columns of the df  : {df_grouped.columns} Example of one patient from the df : {df_grouped[df_grouped['PatientID'] == 1]}'''

    # Query base model
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": user}
        ]
    )

    print(response['message'].content) #print the output

    # Process standard model response
    if not w_model_expert:
        code = traitement_reponse(response['message'].content, model, 'without_expert', lan_logic)
        
    else:
        code = traitement_reponse(response['message'].content, model, model_expert, lan_logic)

        # If multiple expert models provided
        if isinstance(model_expert, list):
            for index in tqdm(range(len(model_expert))):
                try : #to avoid Ollama errors
                    check_expert(model, model_expert[index], code, prompt_system_expert, lan_logic)
                except :
                    print(f'Error with {model_expert[index]}')
                    pass
        else:
            check_expert(model, model_expert, code, prompt_system_expert, lan_logic)


# Validate or correct code with an expert model
def check_expert(model='deepseek-coder-v2', model_expert='deepseek-coder-v2', code='', prompt_system_expert=PROMPT_MODEL_EXPERT, lan_logic='Datalog'):
    if model_expert is None:
        model_expert = model

    # Query expert model
    response = ollama.chat(
        model=model_expert,
        messages=[
            {"role": "system", "content": prompt_system_expert},
            {"role": "user", "content": code}
        ]
    )

    # Process expert model response
    traitement_reponse_expert(response['message'].content, model, model_expert, lan_logic)


# Generate and run a custom diagnosis script for a given patient using the RAG.

import subprocess

def get_code_with_rag(model = 'deepseek-coder-v2', model_expert = 'deepseek-coder-v2', w_model_expert = True, prompt_system = PROMPT_SYSTEM, prompt_system_expert = PROMPT_MODEL_EXPERT, lan_logic = 'Datalog') : 
    
    if vectorstore is None:
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
    user = f'''Now, translate the following criteria into python code between <code> and <\code> and add your explanations for Bipolar I, Bipolar II, Single Episode Depressive Disorder, and Recurrent Depressive Disorder.  {retrieved_context} Relevant symptom names for Observed relation: {df['Observed_Symptom'].unique()}  Relevant condition names for History relation: {df['History_Condition'].unique()}'''
    
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
    return code

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

