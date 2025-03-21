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
### LLM WITH SOUFFLE 
#---

from src import code_Datalog

def traitement_reponse(ollama_output, patient_id=None):
    # Extraction du bloc <explanation>...</explanation>
    explanation_match = re.search(r"<explanation>(.*?)</explanation>", ollama_output, re.DOTALL)
    explanation = explanation_match.group(1).strip() if explanation_match else None

    # Extraction du bloc <code>...</code>
    code_match = re.search(r"<code>(.*?)</code>", ollama_output, re.DOTALL)
    code = code_match.group(1).strip() if code_match else None
    if code:
        with open("code_Datalog.py", "w") as f:
            f.write(code)
    if explanation :
        with open('explanation.txt', 'w') as f : 
            f.write(explanation)
    return(code)

def traitement_reponse_expert(ollama_output, patient_id=None):
    # Extraction du bloc <explanation>...</explanation>
    explanation_match = re.search(r"<rep>(.*?)</rep>", ollama_output, re.DOTALL)
    explanation = explanation_match.group(1).strip() if explanation_match else None

    # Extraction du bloc <code>...</code>
    code_match = re.search(r"<code>(.*?)</code>", ollama_output, re.DOTALL)
    code = code_match.group(1).strip() if code_match else None
    if code:
        with open("code_Datalog_corr.py", "w") as f:
            f.write(code)
    if explanation :
        with open('explanation_expert.txt', 'w') as f : 
            f.write(explanation)

def get_code(model = 'deepseek-coder-v2') : 
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
        {"role": "system", "content": PROMPT_SYSTEM},
        {"role": "user", "content": user}
    ])
    code = traitement_reponse(response['message'].content)
    check_expert(model, code)

def check_expert(model = 'deepseek-coder-v2', code = ''):
    response = ollama.chat(
    model=model,
    messages=[
        {"role": "system", "content": 
PROMPT_MODEL_EXPERT},
        {"role": "user", "content": code}
    ])
    traitement_reponse_expert(response['message'].content)


import os
import subprocess

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


    




